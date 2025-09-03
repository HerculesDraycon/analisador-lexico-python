## Representações dos Tokens

#### NUMBER
`\d` => um dígito de 0 a 9.<br>
`+` = > um ou mais.<br>
`(\.\d*)?` => parte adicional, onde:

&nbsp;&nbsp;&nbsp;&nbsp;`\.` => o ponto literal precisa da contra-barra porque o ponto em regex significa "qualquer caractere".<br>
&nbsp;&nbsp;&nbsp;&nbsp;`\d*` => zero ou mais dígitos.<br>
&nbsp;&nbsp;&nbsp;&nbsp;`(...)` => agrupa.<br>
&nbsp;&nbsp;&nbsp;&nbsp;`(?)` => significa que pode ter ou não.<br>

#### ID
`[A-Za-z_]` => o primeiro caractere deve ser do alfabeto, minúsculo ou maiúsculo ou "_".<br>
`\w*` => depois, pode ter zero ou mais caracteres permitidos.<br>

#### OP
`[...]` => significa qualquer caractere dentro dos colchetes.<br>
`+\-*/` => operadores aritméticos.<br>

#### SKIP
`[ \t]` => espaço ou tabulação.<br>
`+` => um ou mais.<br>

#### MISMATCH
`.` => significa qualquer caractere único.<br>