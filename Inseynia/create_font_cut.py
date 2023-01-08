import pygame
from scripts.loading.json_functions import dump_json, load_json

win = pygame.display.set_mode((1, 1))

f = pygame.image.load("./assets/fontsDL/font.png")

chars = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
'Á', 'É', 'Í', 'Ó', 'Ú', 'À', 'È', 'Ì', 'Ò', 'Ù', 'Â', 'Ê', 'Î', 'Ô', 'Û', 'Ë', 'Ï', 'Ü', 'Ç', 'Ñ', 'á', 'é', 'í', 'ó', 'ú', 'à', 'è', 'ì', 'ò', 'ù', 'â', 'ê', 'î', 'ô', 'û', 'ë', 'ï', 'ü', 'ç', 'ñ', '¡', '¿', 
'أ', 'ب', 'ت', 'ث', 'ج', 'ح', 'خ', 'د', 'ذ', 'ر', 'ز', 'س', 'ش', 'ص', 'ض', 'ط', 'ظ', 'ع', 'غ', 'ف', 'ق', 'ك', 'ل', 'م', 'ن', 'ه', 'و', 'ي', 'ا', 'إ', 'آ', 'ء', 'ؤ', 'ى', 'ئ', 'ة',
'أ1', 'ب1', 'ت1', 'ث1', 'ج1', 'ح1', 'خ1', 'د1', 'ذ1', 'ر1', 'ز1', 'س1', 'ش1', 'ص1', 'ض1', 'ط1', 'ظ1', 'ع1', 'غ1', 'ف1', 'ق1', 'ك1', 'ل1', 'م1', 'ن1', 'ه1', 'و1', 'ي1', 'ا1', 'إ1', 'آ1', 'ء1', 'ؤ1', 'ى1', 'ئ1', 'ة1', 
'أ2', 'ب2', 'ت2', 'ث2', 'ج2', 'ح2', 'خ2', 'د2', 'ذ2', 'ر2', 'ز2', 'س2', 'ش2', 'ص2', 'ض2', 'ط2', 'ظ2', 'ع2', 'غ2', 'ف2', 'ق2', 'ك2', 'ل2', 'م2', 'ن2', 'ه2', 'و2', 'ي2', 'ا2', 'إ2', 'آ2', 'ء2', 'ؤ2', 'ى2', 'ئ2', 'ة2', 
'أ3', 'ب3', 'ت3', 'ث3', 'ج3', 'ح3', 'خ3', 'د3', 'ذ3', 'ر3', 'ز3', 'س3', 'ش3', 'ص3', 'ض3', 'ط3', 'ظ3', 'ع3', 'غ3', 'ف3', 'ق3', 'ك3', 'ل3', 'م3', 'ن3', 'ه3', 'و3', 'ي3', 'ا3', 'إ3', 'آ3', 'ء3', 'ؤ3', 'ى3', 'ئ3', 'ة3', 
'أ4', 'ا4', 'إ4', 'آ4', 'أ5', 'ا5', 'إ5', 'آ5', 
'،', '؟', '٠', '١', '٢', '٣', '٤', '٥', '٦', '٧', '٨', '٩',
'あ', 'い', 'う', 'え', 'お', 'か', 'き', 'く', 'け', 'こ', 'が', 'ぎ', 'ぐ', 'げ', 'ご', 'さ', 'し', 'す', 'せ', 'そ', 'ざ', 'じ', 'ず', 'ぜ', 'ぞ', 'た', 'ち', 'つ', 'て', 'と', 'だ', 'ぢ', 'づ', 'で', 'ど', 'な', 'に', 'ぬ', 'ね', 'の', 'は', 'ひ', 'ふ', 'へ', 'ほ', 'ば', 'び', 'ぶ', 'べ', 'ぼ', 'ぱ', 'ぴ', 'ぷ', 'ぺ', 'ぽ', 'ま', 'み', 'む', 'め', 'も', 'や', 'ゆ', 'よ', 'ら', 'り', 'る', 'れ', 'ろ', 'わ', 'を', 'ん', 'ゃ', 'ゅ', 'ょ', 'っ', 'ぃ',
'ア', 'イ', 'ウ', 'エ', 'オ', 'カ', 'キ', 'ク', 'ケ', 'コ', 'ガ', 'ギ', 'グ', 'ゲ', 'ゴ', 'サ', 'シ', 'ス', 'セ', 'ソ', 'ザ', 'ジ', 'ズ', 'ゼ', 'ゾ', 'タ', 'チ', 'ツ', 'テ', 'ト', 'ダ', 'ヂ', 'ヅ', 'デ', 'ド', 'ナ', 'ニ', 'ヌ', 'ネ', 'ノ', 'ハ', 'ヒ', 'フ', 'ヘ', 'ホ', 'バ', 'ビ', 'ブ', 'ベ', 'ボ', 'パ', 'ピ', 'プ', 'ペ', 'ポ', 'マ', 'ミ', 'ム', 'メ', 'モ', 'ヤ', 'ユ', 'ヨ', 'ラ', 'リ', 'ル', 'レ', 'ロ', 'ワ', 'ヲ', 'ン', 'ャ', 'ュ', 'ョ', 'ッ', 'ィ', 'ー', '。', '、', '・',
'А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ё', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я', 'а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я',
'.', '-', ',', ':', '+', "'", '!', '?', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9' ,'∞' , '(', ')', '/', '_', '=', '\\', '[', ']', '*', '"', '<', '>', ';', '%', "@", "©", "|", '�']
dict = {}

for x in range(f.get_width()):
	c = f.get_at((x, 5))
	if c[0] == 128:
		if len(dict) > 0:
			dict[chars[len(dict)]] = [list(dict.values())[-1][1]+1, x]
		else:
			dict[chars[0]] = [0, x]

dump_json(["./assets/fontsDL/font_cut.json"], dict)