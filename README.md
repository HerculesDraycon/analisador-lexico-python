## Representações dos Tokens

#### COMMENT

`/ /` => casamento de caracter literal.<br>
`\*` => significa o caracter literal "_" que indica que pode ter 0 ou mais elementos no intervalo.<br>
`._?`=>`.`casa qualquer caracter, exceto quebra de linha.`_`0 ou mais.`?`transforma o`_` em lazy ou seja, vai casar o menor trecho possível que ainda permita fechar o padrão, assim, avaliando um por vez, num escopo menor.<br>

#### STRING

`"[^"]*"` => strings delimitadas por aspas duplas, onde:<br>
&nbsp;&nbsp;&nbsp;&nbsp;`"` => aspas duplas literais no início e fim.<br>
&nbsp;&nbsp;&nbsp;&nbsp;`[^"]` => qualquer caractere exceto aspas duplas.<br>
&nbsp;&nbsp;&nbsp;&nbsp;`*` => zero ou mais caracteres permitidos dentro das aspas.<br>

#### CHAR

`'[^']*'` => caracteres delimitados por aspas simples, onde:<br>
&nbsp;&nbsp;&nbsp;&nbsp;`'` => aspas simples literais no início e fim.<br>
&nbsp;&nbsp;&nbsp;&nbsp;`[^']` => qualquer caractere exceto aspas simples.<br>
&nbsp;&nbsp;&nbsp;&nbsp;`*` => zero ou mais caracteres permitidos dentro das aspas.<br>

#### NUMBER

`\d` => um dígito de 0 a 9.<br>
`+` = > um ou mais.<br>
`(\.\d*)?` => parte adicional, onde:

&nbsp;&nbsp;&nbsp;&nbsp;`\.` => o ponto literal precisa da contra-barra porque o ponto em regex significa "qualquer caractere".<br>
&nbsp;&nbsp;&nbsp;&nbsp;`\d*` => zero ou mais dígitos.<br>
&nbsp;&nbsp;&nbsp;&nbsp;`(...)` => agrupa.<br>
&nbsp;&nbsp;&nbsp;&nbsp;`(?)` => significa que pode ter ou não.<br>

`([eE][+-]?\d+)?` => parte opcional (? no final) para a notação científica, onde:

&nbsp;&nbsp;&nbsp;&nbsp;`[eE]` => Corresponde a um único caractere: e ou E.<br>
&nbsp;&nbsp;&nbsp;&nbsp;`[+-]?` => Um sinal opcional que pode ser + ou -.<br>
&nbsp;&nbsp;&nbsp;&nbsp;`\d+` => Um ou mais dígitos, que é o valor do expoente da notação científica.<br>

#### ID

`[A-Za-z_]` => o primeiro caractere deve ser do alfabeto, minúsculo ou maiúsculo ou "\_".<br>
`\w*` => depois, pode ter zero ou mais caracteres permitidos.<br>

#### OP

`[...]` => significa qualquer caractere dentro dos colchetes.<br>
`+\-*/` => operadores aritméticos.<br>
`\b(mod|div)\b` => garante com a boundary que a palavra mod ou div é identificada sozinha.<br>

#### OP_LOGICO

`\b(and|or|not)\b` => operadores de comparação lógica cercados por boundary.

#### OP_RELACIONAL

`<=, >=, <>, <, >, =` => operadores de comparação relacional.

#### CONDITIONAL

`\b(if|then|else)\b` => condicionais cercados por boundary.

#### BLOCK

`\b(begin|end)\b` => blocos de comandos delimitados por begin e end, onde:<br>
&nbsp;&nbsp;&nbsp;&nbsp;`\b` => boundary que garante que as palavras sejam reconhecidas como tokens completos.<br>
&nbsp;&nbsp;&nbsp;&nbsp;`(begin|end)` => alternância entre as palavras-chave "begin" e "end".<br>
&nbsp;&nbsp;&nbsp;&nbsp;`\b` => boundary final para evitar casamento parcial com outras palavras.<br>
`\bread\b` => bloco de leitura read
`\bwrite\b` => bloco de saída write
`\bwriteln\b` => bloco de saída write com quebra de linha

#### LOOP

`\b(while|do)\b` => estruturas de repetição cercadas por boundary.
`\brepeat\b` e `\buntil\b` => estruturas de repetição cercadas por boundary.
`\b(for|to|do)\b` => estruturas do for-to-do cercadas por boundary.

#### ASSIGN

`:=` => token de atribuição.

#### DELIMITER

`[();,:]` => tokens de delimitação do analisador.

#### END PROGRAM

`\.` => token para fim de programa.

#### SKIP

`[ \t]` => espaço ou tabulação.<br>
`+` => um ou mais.<br>

#### MISMATCH

`.` => significa qualquer caractere único.<br>
