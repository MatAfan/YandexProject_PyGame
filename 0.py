songs = {}
singers = []
for i in range(c := int(input())):
    singer = input()
    singers.append(singer)
for i in range(c):
    continuer = False
    song = input()
    for j in song:
        if j.lower() in singers[i].lower():
            continuer = True
            break
    if not continuer:
        if singers[i] in songs:
            songs[singers[i]].append(song)
        else:
            songs[singer[i]] = [song]

for i in songs:
    songs_str = ''
    for j in songs[i]:
        songs_str += j.capitalize() + ', '
    print(f'{i}#{songs_str[:-2]}')