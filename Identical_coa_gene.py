def find_identical_sequences(input_file):
    sequences = {}
    with open(input_file, 'r') as f:
        current_sequence = ''
        current_header = ''
        for line in f:
            line = line.strip()
            if line.startswith('>'):
                if current_sequence:
                    sequences.setdefault(current_sequence, {'count': 0, 'headers': []})
                    sequences[current_sequence]['count'] += 1
                    sequences[current_sequence]['headers'].append(current_header)
                current_header = line[1:]
                current_sequence = ''
            else:
                current_sequence += line
        # Handle the last sequence
        if current_sequence:
            sequences.setdefault(current_sequence, {'count': 0, 'headers': []})
            sequences[current_sequence]['count'] += 1
            sequences[current_sequence]['headers'].append(current_header)
    identical_sequences = {seq: info for seq, info in sequences.items() if info['count'] >= 1}
    return identical_sequences
# Example usage
input_file = "all_coa_sequences.txt"
identical_sequences = find_identical_sequences(input_file)
for seq, info in identical_sequences.items():
    print(f"Sequence: {seq}\tCount: {info['count']}\tHeaders: {', '.join(info['headers'])}")
