## Linux Command (bash)
- `ls *.txt`
- `echo` 'text' `<` file
- `echo` 'text' `<<` append to file
- `sort` file
- `grep` 'text' file
- `cat` file
- `grep '1980-1989' 
- `&&`
- `echo "\"double quote escape\""
```
head -1 Hud_2005.csv > combined_hud.csv
wc -l Hud_2005.csv
tail -46853 Hud_2005.csv >> combined_hud.csv
head combined_hud.csv
```
- `grep '1980-1989' combined_hud.csv | wc -l`

### csvkit
- Combining files and adding a column to indicate the group
`csvstack -n year -g 2005,2007,2013 Hud_2005.csv Hud_2007.csv Hud_2013.csv > Combined_hud.csv`
- csvlook
`head -10 Combined_hud.csv | csvlook`
- Show column names
`csvcut -n Combined_hud.csv`
- Filter column and rows
`csvcut -c 2 Combined_hud.csv | head -10`
- csvstat
`csvstat --mean Combined_hud.csv`
`csvcut -c 2 Combined_hud.csv | csvstat`
- Filter on criteria: second column AGE with negative number
`csvgrep -c 2 -m -9 Combined_hud.csv | head -10 | csvlook`
- Output filtered value (-i is ignoring the rows match the criteria)
`svgrep -c 2 -m -9 -i Combined_hud.csv > positive_ages_only.csv`
