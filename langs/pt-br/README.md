Esta é uma biblioteca simples de simulação de autômatos inspirada por [automata-lib](https://github.com/caleb531/automata) e [automata](https://www.rubydoc.info/gems/automata).

Podemos facilmente construir os autômatos `AFD` (classe `DFA`), `AFND` (classe `NDFA`) e `AP` (não
determinístico, classe`NPDA`) passando como argumento para os respectivos construtores as seguintes
informações:
- o alfabeto de entrada
- os estados do autômato
- o estado inicial
- os estados finais
- as transições (como um `dict`)

Para exemplos, veja [exemplos](#Exemplos)
## Exemplos
- [Construindo Autômatos Finitos Determinísticos](langs/pt-br/examples/dfa.md)
- [Construindo Autômatos Finitos Não Determinísticos](langs/ptbr/examples/ndfa.md)