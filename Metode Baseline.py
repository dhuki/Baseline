def read_dataset(fname):
    sentences = []
    tags = []
    allcontent = []
    with open(fname) as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content]
    idx_line = 0
    while idx_line < len(content):
        sent = []
        tag = []
        temp_content = []
        while not content[idx_line].startswith('</kalimat'):
            if not content[idx_line].startswith('<kalimat'):
                content_part = content[idx_line].split('\t')
                sent.append(content_part[0].lower())
                tag.append(content_part[1])
                temp = content_part[0].lower(),content_part[1]
                temp_content.append(temp)
            idx_line = idx_line + 1
        sentences.append(sent)
        tags.append(tag)
        allcontent.append(temp_content)
        idx_line = idx_line + 2
    return sentences, tags, allcontent

sentences,tags,allcontent = read_dataset('Indonesian_Manually_Tagged_Corpus_ID.tsv')

#split data train and data test --> cutoff = int((0.1 * len(sentences))-3) karena dataset = 1003 kalau int(0.1 * len(sentences))

cutoff = int((0.1 * len(sentences))-3)
training_sentences = sentences[:cutoff]
test_sentences = sentences[cutoff:1020]
#test_sentences = [['ibu','kota','india','mencapai','ribuan']]
training_tags = tags[:cutoff]
test_tags = allcontent[cutoff:1020]

#=================================================================================
# metode baseline

def cekKata(listKata,cekKata): # mengecek apakah kata yang di test sudah di test sebelumnya atau belum
    cek = False

    for m in listkata :
        if (m == cekKata):
            cek = True
            break

    if (cek):
        return True
    else:
        return False

def akurasi(allcontent, test_tag): # mencari akurasi
    count = 0
    for i in allcontent:
        for j in test_tag:
            if (i == j):
                count += 1
                break

    print("Benar : ",count, " / ",len(test_tag))
    print("Total : ", len(allcontent))

    # print(allcontent)
    # print(test_tag)

    return ((count/len(allcontent)) * 100)


Similarity = {}
listkata = []
test_tag2 = []

for i in range(len(test_sentences)):
    for j in range(len(test_sentences[i])):
        if not cekKata(listkata,test_sentences[i][j]): # Digunakan untuk menentukan apaka kata test yang akan diuji sudah diuji sebelumnya atau belum diuji
            for k in range(len(training_sentences)):
                for l in range(len(training_sentences[k])):
                    if (test_sentences[i][j] == training_sentences[k][l]): # menghitung banyaknya hasil tag kata test dari kata train
                        if (test_sentences[i][j],training_tags[k][l]) in Similarity:
                            Similarity[test_sentences[i][j], training_tags[k][l]] += 1
                        else :
                            Similarity[test_sentences[i][j], training_tags[k][l]] = 1
            if (len(Similarity) > 1): # membandingkan tag dari kata test yang mempunyai lebih dari 1 tag untuk ditentukan kata mana yang mempunyai hasil tag tertinggi
                temp = max(Similarity, key=lambda x: x[1])
                test_tag2.append(temp)
            elif (len(Similarity) == 1): # membandingkan tag dari kata test yang hanya mempunyai 1 tag untuk ditentukan kata mana yang mempunyai hasil tag tertinggi
                Similarity["",""] = 0
                temp = max(Similarity, key=lambda x: x[1])
                test_tag2.append(temp)
            else :
                Similarity["", ""] = 0 # jika kata test tidak memiliki tag bedasarkan kata train
                Similarity[test_sentences[i][j], "NN (tidak terdifinisi)"] = 1
                temp = max(Similarity, key=lambda x: x[1])
                test_tag2.append(temp)

            Similarity = {}
            listkata.append(test_sentences[i][j]) # memasukan kata yang sudah di cari tag kata test nya ke sebuah array
        else : # Jika kata test sudah diuji sebelumnya maka tag dari kata test tersebut akan disamakan dengan tag yang sudah diuji sebelumnya
            for m in range(len(test_tag2)):
                if (test_sentences[i][j] == test_tag2[m][0]):
                    test_tag2.append(test_tag2[m])
                    break
    listkata = []

    print("Akutal Tagging : ", test_tags[i])
    print("Prediksi Tagging : ", test_tag2)
    print("Akurasi : ", akurasi(test_tags[i],test_tag2))
    print("=============================================================================================================== Baseline Method")
    print()
    test_tag2 = []
#=================================================================================