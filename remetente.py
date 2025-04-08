#!/usr/bin/env python3
import sys

def calculate_hamming_bits(data):
    """Calcula os bits de paridade do código de Hamming para os dados fornecidos."""
    # Determina o número de bits de paridade necessários
    m = len(data)
    r = 1
    while 2**r < m + r + 1:
        r += 1
    
    # Cria uma lista para o código de Hamming
    hamming = ['0'] * (m + r)
    
    # Preenche os bits de dados nas posições que não são potências de 2
    j = 0
    for i in range(1, m + r + 1):
        if i & (i - 1) != 0:  # Se i não é potência de 2
            hamming[i-1] = data[j]
            j += 1
    
    # Calcula os bits de paridade
    for i in range(r):
        pos = 2**i - 1
        parity = 0
        for j in range(1, m + r + 1):
            if j & (1 << i):
                parity ^= int(hamming[j-1])
        hamming[pos] = str(parity)
    
    return ''.join(hamming)

def create_frame(payload):
    """Cria o frame com cabeçalho, tamanho, payload e terminador."""
    # Adiciona o código de Hamming ao payload
    hamming_payload = calculate_hamming_bits(payload)
    print(f"Payload original: {payload}")  # Debug
    print(f"Payload com Hamming: {hamming_payload}")  # Debug
    
    # Cria o frame
    header = '10101010'  # 0xAA em binário
    size = format(len(hamming_payload) // 8, '08b')  # Tamanho em bytes
    footer = '01010101'  # 0x55 em binário
    
    frame = header + size + hamming_payload + footer
    print(f"Frame completo: {frame}")  # Debug
    return frame

def main():
    if len(sys.argv) != 2:
        print("Uso: python remetente.py <sequencia_de_bits>")
        sys.exit(1)
    
    # Obtém a sequência de bits da linha de comando
    payload = sys.argv[1]
    
    # Verifica se a entrada contém apenas 0s e 1s
    if not all(bit in '01' for bit in payload):
        print("Erro: A entrada deve conter apenas 0s e 1s")
        sys.exit(1)
    
    # Cria e envia o frame
    frame = create_frame(payload)
    sys.stdout.write(frame)  # Usando write em vez de print para evitar nova linha
    sys.stdout.flush()  # Garante que os dados são enviados imediatamente

if __name__ == "__main__":
    main() 