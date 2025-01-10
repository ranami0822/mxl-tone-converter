from music21 import converter, note, chord, stream
import os

def transpose_to_natural(note_obj):
    if isinstance(note_obj, note.Note):
        note_base = note_obj.name
        octave = note_obj.octave
        natural_notes = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
        
        # HをBに変換
        if note_base == 'H':
            note_base = 'B'
        
        # 半音を最も近い自然音に変換
        if note_base in natural_notes:
            return note_base + str(octave)
        if '#' in note_base:
            if note_base[0] == 'E':
                new_note = 'F'
            elif note_base[0] == 'B' or note_base[0] == 'H':
                new_note = 'C'
                octave = str(int(octave) + 1)  # オクターブを1つ上げる
            else:
                new_note = chr(ord(note_base[0]) + 1)
            return new_note + str(octave)
        if 'b' in note_base:
            if note_base[0] == 'C':
                new_note = 'B'
                octave = str(int(octave) - 1)  # オクターブを1つ下げる
            elif note_base[0] == 'F':
                new_note = 'E'
            else:
                new_note = chr(ord(note_base[0]) - 1)
            return new_note + str(octave)
    elif isinstance(note_obj, chord.Chord):
        return [transpose_to_natural(p) for p in note_obj.pitches]
    elif isinstance(note_obj, note.Rest):
        return "Rest"
    return None

def process_mxl(file_path):
    score = converter.parse(file_path)
    for part in score.parts:
        print(f"Part: {part.id}")
        for n in part.flatten().notes:
            if isinstance(n, note.Note):
                original_note = n.nameWithOctave
                new_note = transpose_to_natural(n)
                if new_note is not None:
                    new_note = new_note.replace('H', 'B')  # HをBに変換
                    n.name = new_note[:-1]
                    n.octave = int(new_note[-1])
                    n.addLyric(new_note[:-1])  # 歌詞として音名を追加
                    print(f"Original: {original_note}, Transposed: {new_note}")
            elif isinstance(n, chord.Chord):
                original_note = ' '.join(p.nameWithOctave for p in n.pitches)
                new_notes = transpose_to_natural(n)
                if new_notes is not None:
                    for i, p in enumerate(n.pitches):
                        if new_notes[i] is not None:
                            new_note = new_notes[i].replace('H', 'B')  # HをBに変換
                            p.name = new_note[:-1]
                            p.octave = int(new_note[-1])
                    chord_lyric = ' '.join(p.name for p in n.pitches)
                    n.addLyric(chord_lyric)  # 歌詞として和音の音名を追加
                    print(f"Original: {original_note}, Transposed: {chord_lyric}")
    return score

input_file = input("入力ファイルのパスを入力してください: ")
output_file = os.path.splitext(input_file)[0] + '_transposed.mxl'

transposed_score = process_mxl(input_file)
transposed_score.write('musicxml', fp=output_file)

print(f"変換が完了しました。出力ファイル: {output_file}")