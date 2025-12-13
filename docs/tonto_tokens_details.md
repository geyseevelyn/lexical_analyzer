
# 🔤 Especificação dos *Tokens*

### 1. `KEYWORD`

*Tokens* que representam as **palavras reservadas** da linguagem **TONTO**:

`specializes`, `genset`, `disjoint`, `complete`, `general`, `specifics`, `where`,  
  `package`, `import`, `functional-complexes`, `relators`, `intrinsic-modes`,  
  `extrinsic-modes`, `datatype`, `enum`, `type`, `instanceOf`, `categorizer`,  
  `of`, `relation`, `inverseOf`

---

### 2. `CLASS_STEREOTYPE`

*Tokens* que representam **estereótipos de classes**, usados para definir o tipo ontológico de uma classe:

`event`, `situation`, `process`, `category`, `mixin`, `phaseMixin`, `roleMixin`,  
  `historicalRoleMixin`, `kind`, `collective`, `quantity`, `quality`, `mode`,  
  `intrinsicMode`, `extrinsicMode`, `subkind`, `phase`, `role`, `historicalRole`,  
  `relator`, `class`

--- 

### 3. `RELATION_STEREOTYPE` 

*Tokens* que representam **estereótipos de relações** entre classes,  indicando a natureza e o tipo de vínculo entre entidades ontológicas:

`material`, `derivation`, `comparative`, `mediation`, 
`characterization`, `externalDependence`, `componentOf`, `memberOf`, `subCollectionOf`, `subQualityOf`, `instantiation`, `termination`, `participational`, `participation`, `historicalDependence`, `creation`, `manifestation`, `bringsAbout`, `triggers`, `composition`,`aggregation`, `inherence`, `value`, `formal`, `constitution`

---

### 4. `CLASS_NAME`

*Tokens* que identificam os **nomes de classes**:

- Devem iniciar com letra maiúscula, seguida por qualquer
combinação de letras, ou tendo sublinhado como subcadeia própria, sem números.

🔹 *Exemplos:*  
```tonto
class Person
class UniversityCampus
class Car_Rental
```

---

### 5. `RELATION_NAME`

*Tokens* que identificam os nomes de **relações** entre classes: 

- Devem começar com letra minúscula, seguida por qualquer
combinação de letras, podendo conter sublinhado como subcadeia própria, mas sem números. 

🔹 *Exemplos:*  
```tonto
has, hasParent, has_parent, isPartOf, is_part_of
```
---

### 6. `INSTANCE_NAME`

*Tokens* que que identificam os nomes de **instâncias** da ontologia: 

- Iniciam com qualquer letra, podendo ter o sublinhado como subcadeia própria e **terminando com algum número inteiro**. 

🔹 *Exemplos:*  
```tonto
Planet1, Planet2 pizza03, car123
```
---

### 7. `ATTRIBUTE`

*Tokens* que identificam **atributos** de *Classes* e *DataTypes*:

- Devem começar com letra minúscula, seguida por qualquer combinação de letras ou sublinhado como subcadeia própria, mas sem números. **Devem terminar em** `:`.

🔹 *Exemplos:*  
```tonto
name:, age:, birthDate:, phoneNumber:
```

---

### 8. `META_ATTRIBUTE`

*Tokens* que que representam os **meta-atributos** da linguagem **TONTO**:

`ordered`, `const`, `derived`, `subsets`, `redefines`

---

### 9. `NATIVE_DATATYPE`

*Tokens* que representam os **tipos de dados nativos** aceitos na linguagem **TONTO**:

`number`, `string`, `boolean`, `date`, `time`, `datetime`

---

### 10. `NEW_DATATYPE`

*Tokens* que identificam **novos tipos de dados personalizados**, criados pelo usuário:

- Começam com letras, sem números, sem sublinhado e devem terminar com a subcadeia `DataType`.

🔹 *Exemplo:*  
```tonto
CPFDataType, PhoneNumberDataType, AddressDataType
```
 
---

### 11. `SPECIAL_SYMBOL`

*Tokens* que representam **símbolos especiais** da sintaxe **TONTO**, usados para delimitar, agrupar ou indicar relações entre elementos:

`{`, `}`, `(`, `)`, `[`, `]`, `..`, `,`, `*`, `@`, `:`, `--`, `<>--`, `--<>`, `<o>--`, `--<o>`

---

### 12. `CARDINALITY`

*Tokens* que especificam **restrições de multiplicidade** em relações ou atributos.  

- Podem assumir formatos como `[n]`, `[n..m]`, `[n..*]`, ou `[*]`.

🔹 *Exemplo:*  
```tonto
relation hasStudent [1..*]
relation teaches [0..1]
```