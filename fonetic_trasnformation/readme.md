# Fonetická transkripce

Jméno a Příjmení: Daniel Cífka\
Osobní číslo: A23N0100P\
Předmět KKY/HDS -> 1.SP Fonetická transkripce\

## Spuštění

```cmd
python Main.py -inputfile <vstupní soubor> -outputfile <výstupní soubor>
```

- <vstupní soubor> -> je uveden název vstupního souboru/cesta ke vstupnímu souboru
- <výstupní soubor> -> je uveden název výstupního souboru/cesta ke výstupnímu souboru

## Popis algoritmu

1. Funkce ```data_loader()``` načte jednotlivé řádky ze souboru
2. Dale se zavolá funkce ```preprocesing()```, která
    - odstraní nepotřebné značeky,
    - nahradí interpukce za požadované značky, 
    - vratí seznam takto přezpracovaných textů.
3. Po předzpracování dojde k jádru celého skriptu a to k samostatné fonetické transkripci, kde jsou pomocí příkazů if a elif aplikovány fonetická pravidla pro přepis do fonetické podoby textu.
    - Následující sekci budou uvedena pravidla nebo jejich část, která ve skriptu nebyla použita.
    - Metoda zpraující tyto pravidla se nazývá ```check_rulles()```.
    - Návratovou hodnout z této funkce je seznam velikosti počtu znaků ve větě, kde jsou zavedené převedené prvky podle pravidel a na ostatních místech je hodnota None.
4. Poslední částí skriptu je volání funkce ```final_preprocesing_and_write()```, která 
    - převede elementy None na znaky z původní věty a spojuje to do stringové podoby věty,
    - provede převod znaků na znaky v EPA abecedě
    - převod unikátních slov na jejich správnou podobu
    - nakonec tuto upravenou větu zapíše do zvoleného výstupního souboru.

## Nevyužitá fonetická pravidla

- ZPK -> ¬ZPK / _<+JK>,
- ZPK -> ZPK / _<+JK>,
- ZPK1 -> ZPK1 / <"JPZ"> _<-ZPK2, -JK>,
- t -> ť / _<ň>,
- t -> t / _<ň>,
- d -> ď / _<ň>,
- d -> d / _<ň>,
- n -> ň / _ <ť, ď>,
- n -> n / _ <ť, ď>,
- t-š -> tš,
- t|š -> tš,
- tš -> č,
- tš -> tš,
- d-z -> dz,
- d|z -> dz,
- dz -> dz,
- d-ž -> dž,
- d|ž -> dž,
- dž -> dž,
- zští -> šťí / _ |,
- zští -> sšťí / _ |,
- žští -> šťí / _ |,
- žští -> ššťí / _ |,
- ť -> t / š _ k,
- ť -> ť / š _ k,
- d -> d / z _ <"n, ň">,
- d -> i / z _ <"n, ň">,
- vz -> z / <|, - ,> _ <-b, -p>,
- fs -> s / <|, - ,>_<-b, -p>,
- Výslovnost dvou foneticky stejných souhlásek (všechna pravidla)