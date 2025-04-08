#!/usr/bin/env python3
import sys

def calculate_hamming_bits(data):
    """Calcula os bits de paridade do código de Hamming para os dados fornecidos."""
    m = len(data)
    r = 1
    while 2**r < m + r + 1:
        r += 1
    
    hamming = ['0'] * (m + r)

    j = 0
    for i in range(1, m + r + 1):
        if i & (i - 1) != 0:
            hamming[i-1] = data[j]
            j += 1

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
    hamming_payload = calculate_hamming_bits(payload)
    
    # Prints de debug vão para stderr
    print(f"Payload original: {payload}", file=sys.stderr)
    print(f"Payload com Hamming: {hamming_payload}", file=sys.stderr)

    header = '10101010'  # 0xAA
    size = format(len(hamming_payload) // 8, '08b')  # Tamanho em bytes
    footer = '01010101'  # 0x55

    frame = header + size + hamming_payload + footer
    print(f"Frame completo: {frame}", file=sys.stderr)

    return frame

def main():
    if len(sys.argv) != 2:
        print("Uso: python remetente.py <sequencia_de_bits>", file=sys.stderr)
        sys.exit(1)

    payload = sys.argv[1]

    if not all(bit in '01' for bit in payload):
        print("Erro: A entrada deve conter apenas 0s e 1s", file=sys.stderr)
        sys.exit(1)

    frame = create_frame(payload)
    
    # Apenas o frame vai para stdout
    sys.stdout.write(frame)
    sys.stdout.flush()

if __name__ == "__main__":
    main()
