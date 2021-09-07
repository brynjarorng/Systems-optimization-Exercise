
from bs4 import BeautifulSoup
 
with open('dict.xml', 'r') as f:
    data = f.read()
 
Bs_data = BeautifulSoup(data, "xml")

b_unique = Bs_data.find_all('unique')
 
print(b_unique)
 
b_name = Bs_data.find('child', {'name':'Frank'})
 
print(b_name)
 
value = b_name.get('test')
 
print(value)