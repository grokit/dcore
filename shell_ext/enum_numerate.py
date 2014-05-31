
enum ="""
enum tata
{
    a,
    b,
    c
}
"""

out = []

i = 0
for line in enum.splitlines():
    
    if line.find(',') != -1:
        line = line.replace(',', ' = %s,' % i)
        i += 1
    
    out.append(line)

print("\n".join(out))
    
        
        
