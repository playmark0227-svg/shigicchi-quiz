import re, json, pathlib
root=pathlib.Path(__file__).resolve().parent.parent
s=(root/'source/original.txt').read_text(encoding='utf-8-sig')
parts=re.split(r'問題[：:]',s)[2:]
questions=[]
for i,p in enumerate(parts,1):
    q,body=re.split(r'解答[：:]',p,maxsplit=1)
    body=body.split('—---')[0].split('________________')[0]
    before,_,after=body.partition('画像があるならここに→')
    lines=[x.strip() for x in before.splitlines() if x.strip()]
    answer=lines[0] if lines and not re.match(r'^1[.．]',lines[0]) else ''
    options=re.findall(r'^\s*[1-4][.．]?\s*(.+?)\s*$', '\n'.join(lines[1:] if answer else lines),re.M)
    explanation=re.split(r'解説[：:]',before)[1] if re.search(r'解説[：:]',before) else after
    explanation=re.sub(r'^解説[：:]','',explanation.strip()).strip()
    questions.append(dict(id=i,question=re.sub(r'\s+','',q),options=options,answer=answer,explanation=explanation,image=f'assets/q{i:02}.webp',active=True))

def setq(i,**kw): questions[i-1].update(kw)
def hold(i,reason): setq(i,active=False,review=reason)

setq(1,question='このクイズで使うトイレの「大」レバー。1回で流す水の量は？',correct=[2],explanation='この問題では6〜8リットル。トイレの種類や作られた年によって、使う水の量はちがうよ。')
hold(1,'使用水量は便器の機種による。想定機種の確認が必要。')
setq(2,options=['流氷','氷島','氷流','氷河'],correct=[0])
setq(3,question='網走市の水道の水は、主にどこから来るでしょうか？',options=['藻琴山（もことやま）のわき水や地下水','海の水','湖の水','おうちの人が買ってくる水'],correct=[0],explanation='網走市の水道は、藻琴山のわき水や地下水を主な水源にしているよ。',revision='市公式資料に合わせ、原稿の「川」を「わき水や地下水」に修正。',sources=['https://www.city.abashiri.hokkaido.jp/uploaded/attachment/1732.pdf'])
setq(4,question='ごみをへらすことを「リサイクル」という。○か×か？',options=['○','×'],correct=[1],explanation='ごみをへらすことは「リデュース」。リサイクルは、ごみを加工して、もう一度資源として使うことだよ。')
setq(5,correct=[3])
setq(6,correct=[0],explanation='りんごは木に実がなるよ。赤く実ったりんごを、枝から収穫するんだ。',revision='原稿の正解番号2を1へ修正。')
setq(7,correct=[1])
hold(8,'水を飲まない場合の生存日数は環境や体調で異なり、4日と断定できない。')
setq(9,options=['酪農（らくのう）','畑作（はたさく）'],correct=[0])
hold(9,'酪農と畑作の比較基準が未指定。地域の範囲と原稿の酪農という正解を要確認。')
setq(10,correct=[2],explanation='きゅうりは、約95%が水分でできているよ。')
setq(11,correct=[1])
setq(12,question='北海道の2025年度の調査で、農作物などへのひがいの金額がいちばん大きかった動物はどれ？',correct=[1],explanation='エゾシカは、畑の作物や森の木を食べてしまうことがあるんだ。',revision='地域・年度・ひがいの金額という比較基準を補足。',sources=['https://www.pref.hokkaido.lg.jp/ks/skn/higai.html'])
setq(13,question='イヌは、人間のように全身からたくさんあせをかいて、体を冷やす。○か×か？',options=['○','×'],correct=[1],explanation='イヌは、主に口を開けてハアハアと息をすることで体を冷やすよ。肉球などには、あせを出すしくみもあるんだ。',revision='犬は汗を全くかかないという説明を修正。',sources=['https://www.minamigaokaah.com/communication/column/2020/09/post_602.html'])
setq(14,correct=[0])
setq(15,correct=[0])
setq(16,question='運動のあと、あせで失った水分や、使ったエネルギーを補うものを3つ選ぼう。',correct=[0,1,2],multi=True,explanation='水分と塩分、エネルギーになる糖分だよ。長く運動してたくさんあせをかいたとき、スポーツドリンクなどで補えるよ。')
hold(16,'運動の強さや時間によって補給内容は異なる。児童向けの健康指導として授業担当者の確認待ち。')
setq(17,correct=[1],explanation='つぶつぶは、実（果実）なんだ！ その小さな実の中に、種が入っているよ。',revision='原稿の正解「種」を「実」に修正。',sources=['https://www.maff.go.jp/j/pr/aff/1912/spe1_02.html'])
setq(18,correct=[0])
setq(19,correct=[1]);hold(19,'脱水症状の定義と数値の根拠を授業担当者に確認。')
setq(20,question='オホーツク地域でさかんな、海の仕事と畑の仕事の組み合わせはどれ？',options=['漁業と畑作','林業と稲作','果樹栽培と林業'],correct=[0],revision='自由回答をタッチで選べる3択に整理。')
setq(21,correct=[0]);hold(21,'「初めに感染」の定義とインフルエンザの種類が不明。')
setq(22,options=['○','×'],correct=[0],explanation='ペンギンは鳥のなかま。「鳥類（ちょうるい）」に入るよ。空は飛べないけれど、泳ぐのがとても得意！')
setq(23,question='濤沸湖（とうふつこ）水鳥・湿地センターがあるのは、どの湖のそば？',correct=[1],revision='空欄の正解を施設の公式情報から補完。',sources=['https://www.env.go.jp/nature/ramsar/conv/waterfowl/toufutsuko.html'])
setq(24,question='能取湖（のとろこ）のまわりを、秋に真っ赤にそめる植物は何？',options=['サンゴ草（アッケシソウ）','モミジ','ヒマワリ','マリモ'],correct=[0],revision='長文を短い問いに整理。能取湖の読みを修正。',sources=['https://www.pref.hokkaido.lg.jp/kn/tkn/hana/place/o014.html'])
setq(25,correct=[]);hold(25,'正解欄が空欄。リサイクル品は製品と素材の確認が必要。')
setq(26,question='短い時間に、水を大量に飲むのは体によい。○か×か？',options=['○','×'],correct=[1],explanation='水分は、こまめにとろう。一度に大量の水を飲むと、体の塩分のバランスがくずれて危険なことがあるよ。',revision='原稿の解説に合わせて正解を×へ修正。')
hold(26,'健康問題のため、修正文と正解を授業担当者に確認後に出題。')
setq(27,correct=[0],explanation='サケには、人間のようなまぶたがないよ。水の中では、空気中のように目がかわかないんだ。')
setq(28,correct=[1]);hold(28,'睡眠中の発汗量は体格や環境で変わる。数値の根拠確認待ち。')
setq(29,question='この中で、ラムサール条約に登録されている湿地の湖はどれ？',correct=[1],sources=['https://www.env.go.jp/nature/ramsar/conv/waterfowl/toufutsuko.html'])
setq(30,options=[],correct=[]);hold(30,'「これ」に当たる実物画像が未添付。画像から材質を断定できないため保留。')
setq(31,correct=[2])
setq(32,options=['○','×'],correct=[0],explanation='成虫になると、口が退化して何も食べないガもいるよ。幼虫のときにたくわえた栄養で生きるんだ。')
setq(33,question='クラゲにさされたことが、納豆アレルギーのきっかけになる場合がある。○か×か？',options=['○','×'],correct=[0],explanation='クラゲと納豆に共通する成分が原因になる場合があるよ。さされた人が全員アレルギーになるわけではないんだ。',sources=['https://www.jstage.jst.go.jp/article/jspaci/37/1/37_60/_article/-char/ja/'],revision='必ず発症するという誤解を避ける表現へ修正。')
setq(34,question='塩分のある場所でも育つ「塩生植物（えんせいしょくぶつ）」。秋に赤くなるのはどれ？',correct=[2],revision='絶滅危惧種の区分の断定を避けて整理。')
setq(35,correct=[2]);hold(35,'選択肢の健康効果を一律に断定できないため保留。')
setq(36,correct=[2]);hold(36,'統計の年度・ごみの定義・出典が未指定。')
setq(37,correct=[0],options=['中国','日本','アメリカ']);hold(37,'統計の年度・ごみの定義・出典が未指定。')
setq(38,correct=[2]);hold(38,'統計の年度・ごみの定義・出典が未指定。')
setq(39,correct=[2]);hold(39,'統計の年度・ごみの定義・出典が未指定。')
setq(40,question='海をよごすごみのうち、細かくくだけても自然に分解されにくいものはどれ？',correct=[0])
setq(41,options=['5mmより小さいプラスチック','マイクロソフトのごみ','マイクロフォンのごみ'],correct=[0],explanation='とても小さくなったプラスチックだよ。海に流れ出ると、集めるのがむずかしいんだ。',revision='「5mm以下」を「5mmより小さい」に修正。',sources=['https://www.gov-online.go.jp/article/202510/entry-9675.html'])
for q in questions:
    q['category']='水とくらし' if q['id'] in [1,3,5,8,10,16,19,26,28,35] else '地球とごみ' if q['id'] in [4,14,25,30,36,37,38,39,40,41] else '自然といきもの' if q['id'] in [2,12,13,21,22,23,24,27,29,31,32,33,34] else '食べものと農業'
    q['explanation']=re.sub(r'\s+','',q['explanation'])
    if q['active']:
        assert 2 <= len(q['options']) <= 4 and len(set(q['options'])) == len(q['options']), q
        assert q['correct'] and all(c<len(q['options']) for c in q['correct']),q
(root/'questions.json').write_text(json.dumps(questions,ensure_ascii=False,indent=2))
print(len(questions),'total;',sum(q['active'] for q in questions),'active')
