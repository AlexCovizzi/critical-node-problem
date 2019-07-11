
%{ removed(X) : nodo(X) } = K :- rem(K).

%adiacente(X, Y) :- { arco(X,Y) ; arco(Y, X) } > 0, nodo(X), nodo(Y), not removed(X), not removed(Y), X < Y.

%connesso(X, Y) :- nodo(X), nodo(Y), X < Y, adiacente(X, Y).
%connesso(X, Y) :- nodo(X), nodo(Y), nodo(Z), X < Y, { adiacente(X, Z) ; adiacente(Z, X) } > 0, { connesso(Y, Z) ; connesso(Z, Y) } > 0.

%{ componente(X) } :- nodo(X), not removed(X).

%:- componente(X), componente(Y), X != Y, { connesso(X, Y) ; connesso(Y,X) } > 0.

%conta(N) :- N = { componente(X) }.

%#maximize { 1, X : componente(X) }.

%#show removed/1.
%#show componente/1.
%#show conta/1.

{ removed(X) : nodo(X) } = K :- rem(K).

adiacente(X, Y) :- arco(X, Y), not removed(X), not removed(Y).
adiacente(X, Y) :- arco(Y, X), not removed(X), not removed(Y).

connesso(X, Y) :- X < Y, adiacente(X, Y).
connesso(X, Y) :- X < Y, Y < Z, adiacente(X, Z), connesso(Y, Z).
connesso(X, Y) :- X < Y, Y > Z, adiacente(X, Z), connesso(Z, Y).

componente(X) :- nodo(X), not removed(X), not connesso(_, X).

conta(N) :- N = #count{ 1, X : componente(X) }.

#maximize { 1, X : componente(X) }.

#show removed/1.
#show componente/1.
#show conta/1.