array[1..n] of var 0.0 .. 1.0: v;
array[1..n,1..n] of var 0.0 .. 1.0: u;

% La matrice u è triangolare superiore
constraint forall(i in 1..n) (u[i,i] = 1);
constraint forall(i,j in 1..n where i < j) (u[i,j] = u[j,i]);

% Vincoli sulla connessione dei nodi
constraint forall (i,j in 1..n where i < j)
              (if E[i,j] = 1 then u[i,j] + v[i] + v[j] >= 1
              else u[i,j] >= 0 endif);
              
constraint forall (i,j,w in 1..n where i < j)
              (u[i,j] + u[j,w] - u[w,i] <= 1) ;

constraint forall (i,j,w in 1..n where i < j)
              (u[i,j] - u[j,w] + u[w,i] <= 1) ;

constraint forall (i,j,w in 1..n where i < j)
              (- u[i,j] + u[j,w] + u[w,i] <= 1) ;

% Vincolo di cardinalità
constraint sum(v) <= k;

% Minimizzo la somma degli elementi di u
solve minimize sum(u);

output [show(v), "\n", show(sum(u))];