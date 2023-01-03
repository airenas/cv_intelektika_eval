# Intelektika.lt transcription service evaluation

Evaluation of Intelektika.lt transcription service on Common Voice Dataset

## Steps to estimate WER

1. install python requirements
```bash
pip install -r requirements.txt
```

2. evaluate
```bash
make eval/wer
```

## Results

Used *test.tsv* file of the [Common Voice Dataset](https://commonvoice.mozilla.org/en/datasets) Lithuanian subset

|Version|WER|Sentemces|Words|Err all|Subst|Del|Ins|
|-|-|-|-|-|-|-|-|
|Common Voice Corpus 12.0|6.96%|3785|25370|1768|1422|156|190|

## Samples

```bash
make eval/cmp n=20
PYTHONPATH=./ LOG_LEVEL=INFO python src/cmp.py --ref work/ref.txt --pred work/predicted.txt --n 20

reference: Aštuonios salos vadinamos „pagrindinėmis“ arba „didžiosiomis“ salomis.
predicted: Aštuonios salos vadinamos pagrindinėmis arba didžiosiomis salomis.
---
reference: Miesto centre veikia seniausia pasaulyje fondų birža.
predicted: Miesto centre veikia seniausia pasaulyje fondų birža,
---
reference: Dramblių smegenys gerai išsivysčiusios.
predicted: Dramblio smegenys gerai išsivysčiusios.
---
reference: Papėdėje yra piroklastų skydas su lavos kupolais.
predicted: Papėdėje yra piroklastinių skydas su lavos kupolais.
---
reference: Tai pabaigė pilietinį karą.
predicted: Kaip avalynę,
---
reference: Kiaušinėlius deda du kartus.
predicted: Balkone kiaušinėlius deda du kartus, esą medikės buvo mažuma.
---
reference: Cerkvės klebonu buvo paskirtas kunigas Aleksandr Mackevič.
predicted: Cerkvės klebonu buvo paskirtas kunigas Aleksandras Mackevič.
---
reference: Dabar skiria Ciešino Sileziją nuo Mažosios Lenkijos.
predicted: Dabar skiria C. <šino> Sileziją nuo Mažosios Lenkijos.
---
reference: Pirmąją kompoziciją šeimoje sukūrė būdamas dešimties.
predicted: Pirmojo kompoziciją šeimoje sukūriau būdamas dešimties.
---
reference: Paplitusios drėgname ir sūriame vandenyje nuo Indijos iki Japonijos.
predicted: Paplitusios drėgname ir sūriame vandenyje, nuo Indijos iki Japonijos,
---
reference: Ji tuo metu pagal savo teisinę formą buvo akcinė bendrovė.
predicted: Ji tuo metu pagal savo teisinę formą buvo akcinė bendrovė.
---
reference: Knygų leidimo komisijos steigėjas.
predicted: Knygų leidimo komisijos steigėjas -
---
reference: Vėliau išleido dar kelias knygas.
predicted: Vėliau išleido dar kelias knygas,
---
reference: Leido ir redagavo Stasys Jokubauskas.
predicted: Leido ir redagavo Stasys Jakubauskas,
---
reference: Jau Pirmojo pasaulinio karo pradžioje jis buvo tarp aukščiausio rango lenkų karininkų.
predicted: Jau Pirmojo pasaulinio karo pradžioje jis buvo tarp aukščiausio rango lenkų karininkų.
---
reference: Apylinkėse auginamos vynuogės.
predicted: Apylinkėse auginamos vynuogės.
---
reference: Didžiąją dalį leidyklos leidžiamos mokomosios literatūros rengia šalies autoriai.
predicted: Didžiąją dalį leidyklos leidžiamos mokomosios literatūros rengia šalies autoriai.
---
reference: Svarbus tekstilės ir kitų audinių centras.
predicted: Svarbus tekstilės ir kitų audinių centras,
---
reference: Varžyboms teisėjauja du teisėjai.
predicted: Varžyboms teisėjavę teisėjai,
---
reference: Floridos provincijos centras.
predicted: Floridos provincijos centras,
---
```

