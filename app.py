from flask import Flask, render_template, request

from main import window

# Flask uygulamasını oluşturma
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home(sg=None, districts=None, candidates=None):
    if request.method == 'POST':
        # İlçeler ve sandık sayıları
        districts = {
            'Altınova': {'start': 1001, 'end': 1072, 'total': 72},
            'Armutlu': {'start': 1001, 'end': 1027, 'total': 27},
            'Çiftlikköy': {'start': 1001, 'end': 1103, 'total': 103},
            'Termal': {'start': 1001, 'end': 1013, 'total': 13},
            'Çınarcık': {'start': 1001, 'end': 1084, 'total': 84},
            'Merkez': {'start': 1001, 'end': 1289, 'total': 289}
        }

        # Adaylar
        candidates = ['Recep Tayyip Erdoğan', 'Kemal Kılıçdaroğlu']

        # İlçelerdeki oy sayıları
        district_votes = {district: {candidate: 0 for candidate in candidates} for district in districts}

        # Toplam oy sayıları
        total_votes = {candidate: 0 for candidate in candidates}

        # Adayların ilçelerdeki oy oranları
        district_vote_percentages = {district: {candidate: 0 for candidate in candidates} for district in districts}

        # Adayların toplam oy oranları
        total_vote_percentages = {candidate: 0 for candidate in candidates}

        # Sandık numaralarını oluşturma
        def generate_ballot_numbers(start, end):
            return [str(i) for i in range(start, end + 1)]

        # Oy oranlarını hesapla
        def calculate_vote_percentages():
            for district, votes in district_votes.items():
                total = sum(votes.values())
                for candidate, vote_count in votes.items():
                    if total != 0:
                        district_vote_percentages[district][candidate] = (vote_count / total) * 100
                    else:
                        district_vote_percentages[district][candidate] = 0

            total_vote_count = sum(total_votes.values())
            for candidate, vote_count in total_votes.items():
                if total_vote_count != 0:
                    total_vote_percentages[candidate] = (vote_count / total_vote_count) * 100
                else:
                    total_vote_percentages[candidate] = 0

        # Ana döngü
        while True:
            event, values = window.read()
            if event == sg.WINDOW_CLOSED:
                break
            elif event == 'district_combo':
                selected_district = values['district_combo']
                start = districts[selected_district]['start']
                end = districts[selected_district]['end']
                sandik_numaralari = generate_ballot_numbers(start, end)
                window['box'].update(values=sandik_numaralari)
            elif event in ('erdogan_votes', 'kilicdaroglu_votes'):
                try:
                    erdogan_votes = int(values['erdogan_votes'])
                    kilicdaroglu_votes = int(values['kilicdaroglu_votes'])
                    selected_district = values['district_combo']
                    district_votes[selected_district]['Recep Tayyip Erdoğan'] = erdogan_votes
                    district_votes[selected_district]['Kemal Kılıçdaroğlu'] = kilicdaroglu_votes
                    total_votes['Recep Tayyip Erdoğan'] = sum(
                        votes['Recep Tayyip Erdoğan'] for votes in district_votes.values())
                    total_votes['Kemal Kılıçdaroğlu'] = sum(
                        votes['Kemal Kılıçdaroğlu'] for votes in district_votes.values())
                    calculate_vote_percentages()
                except ValueError:
                    pass
            elif event == 'Sonucu Gör':
                result_text = ''
                for district, votes in district_vote_percentages.items():
                    result_text += f'{district}:\n'
                    for candidate, percentage in votes.items():
                        result_text += f'{candidate}: %{percentage:.2f}\n'
                    result_text += '\n'
                total_result_text = ''
                for candidate, percentage in total_vote_percentages.items():
                    total_result_text += f'{candidate}: %{percentage:.2f}\n'
                window['result'].update(result_text)
                window['total_result'].update(total_result_text)

        window.close()
        # Form verilerini alın ve gerekli işlemleri yapın
        selected_district = request.form.get('district_combo')
        erdogan_votes = int(request.form.get('erdogan_votes'))
        kilicdaroglu_votes = int(request.form.get('kilicdaroglu_votes'))
        # Diğer işlemler ve sonuçları hesaplama

        return render_template('result.html', result_text=result_text, total_result_text=total_result_text)
    else:
        return render_template('index.html', districts=districts, candidates=candidates)


if __name__ == '__main__':
    app.run(debug=True)
