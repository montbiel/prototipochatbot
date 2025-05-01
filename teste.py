bebidas = []
for i in range(5):  # vai pedir 5 bebidas
    bebida = input("Digite o nome da bebida: ")
    bebidas.append(bebida)

print("\nLista de bebidas:")
for bebida in sorted(bebidas):
    print(f"- {bebida}")


