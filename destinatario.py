#!/usr/bin/env python3
import sys

def correct_hamming_error(hamming_code):
    """Detecta e corrige erros de 1 bit no código de Hamming."""
    # Determina o número de bits de paridade
    r = 0
    while 2**r < len(hamming_code):
        r += 1
    
    # Calcula a posição do erro
    error_pos = 0
    for i in range(r):
        parity = 0
        for j in range(1, len(hamming_code) + 1):
            if j & (1 << i):
                parity ^= int(hamming_code[j-1])
        if parity:
            error_pos += 2**i
    
    # Corrige o erro se encontrado
    if error_pos > 0:
        print(f"Erro detectado na posição {error_pos}")
        corrected = list(hamming_code)
        corrected[error_pos-1] = '1' if corrected[error_pos-1] == '0' else '0'
        hamming_code = ''.join(corrected)
    
    # Extrai os bits de dados
    data = []
    for i in range(1, len(hamming_code) + 1):
        if i & (i - 1) != 0:  # Se i não é potência de 2
            data.append(hamming_code[i-1])
    
    return ''.join(data)

def decode_frame(frame):
    """Decodifica o frame e extrai o payload."""
    print(f"Frame recebido: {frame}")  # Debug
    
    # Verifica o cabeçalho
    header = frame[:8]
    print(f"Cabeçalho: {header}")  # Debug
    if header != '10101010':
        print("Erro: Cabeçalho inválido")
        sys.exit(1)
    
    # Extrai o tamanho do payload
    size = int(frame[8:16], 2)
    print(f"Tamanho do payload: {size} bytes")  # Debug
    
    # Extrai o payload com código de Hamming
    hamming_payload = frame[16:-8]
    print(f"Payload com Hamming: {hamming_payload}")  # Debug
    
    # Verifica o terminador
    footer = frame[-8:]
    print(f"Terminador: {footer}")  # Debug
    if footer != '01010101':
        print("Erro: Terminador inválido")
        sys.exit(1)
    
    # Corrige erros e extrai o payload original
    payload = correct_hamming_error(hamming_payload)
    return payload

def main():
    # Lê o frame do stdin
    frame = sys.stdin.read().strip()
    if not frame:
        print("Erro: Nenhum dado recebido do stdin")
        sys.exit(1)
    
    # Decodifica o frame e exibe o payload
    payload = decode_frame(frame)
    print(f"Payload final: {payload}")

if __name__ == "__main__":
    main() 