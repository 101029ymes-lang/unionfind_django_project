from django.core.management.base import BaseCommand
from quiz.models import Question, Choice


class Command(BaseCommand):
    help = '匯入第九章不相交集合題庫'

    def handle(self, *args, **options):
        data = [('下列的資料結構中，何者的基本操作包含 Find 與 Union？', ['堆疊', '佇列', '優先佇列', '不相交集合', '以上皆非'], '不相交集合', '不相交集合（Disjoint Set）又常被稱為 Union-Find 資料結構，其兩大核心操作即為合併（Union）與查詢（Find）。', False, 'easy'), ('「不相交集合」中，Find 的操作目的為何？', ['搜尋某單筆的資料', '求不相交集合的個數', '找到集合的代表', '搜尋排序位置', '以上皆非'], '找到集合的代表', 'Find 操作用於尋找該元素所屬集合的根節點（即代表元素），主要用來判斷兩個不同元素是否屬於同一個集合。', False, 'easy'), ('「不相交集合」中，Union 的操作目的為何？', ['搜尋某單筆的資料', '取聯集', '取交集', '取差集', '以上皆非'], '取聯集', 'Union 操作的作用是將兩個原本不相交的集合合併成一個新的集合，概念上等同於數學集合操作中的取聯集。', False, 'easy'), ('「不相交集合」中，每個元素剛開始的代表為何？', ['一個是先定義的根節點', '元素本身', '集合中第一個元素', '集合中最後的元素'], '元素本身', '在初始化的建立階段（Make-Set），每個元素都會各自形成一個獨立的集合，並預設將自己設為該集合的代表。', False, 'easy'), ('「不相交集合」通常是使用下列哪種資料結構實現？', ['陣列', '堆疊', '佇列', '二元樹', '以上皆非'], '陣列', '不相交集合最常使用一維陣列來實作，利用陣列索引代表節點，陣列值記錄父節點位置。', False, 'easy'), ('下列資料結構中，何者適合用來實現迷宮產生器，以確保起點與終點的路徑一定存在？', ['堆疊', '佇列', '優先佇列', '不相交集合', '以上皆非'], '不相交集合', '迷宮產生器可利用不相交集合隨機打通相鄰牆壁，直到確認起點與終點在同一連通集合。', False, 'medium'), ('下列資料結構中，何者適合用來解連通元問題？', ['堆疊', '佇列', '優先佇列', '不相交集合', '以上皆非'], '不相交集合', '不相交集合能高效處理圖形中頂點的合併與分組，是解決無向圖連通元問題的常見方法。', False, 'medium'), ('Path Compression（路徑壓縮）的主要作用為何？', ['將集合拆成多個集合', '在 Find 過程中讓節點直接指向代表節點', '依照元素大小排序', '刪除集合中的元素'], '在 Find 過程中讓節點直接指向代表節點', 'Path Compression 會在 Find 過程中讓路徑上的節點直接指向代表節點，以降低之後查詢時間。', True, 'medium'), ('Union by Rank 或 Union by Size 的主要目的為何？', ['讓選項隨機排列', '盡量降低樹的高度，使 Find 更有效率', '將資料轉成佇列', '保證所有元素按照數字排序'], '盡量降低樹的高度，使 Find 更有效率', 'Union by Rank 或 Size 會讓較小或較矮的樹接到較大的樹底下，以降低樹高。', True, 'medium'), ('判斷兩個元素 x、y 是否屬於同一集合，最常用的方式為何？', ['x + y 是否為偶數', 'x 與 y 的陣列位置是否相鄰', 'Find(x) 是否等於 Find(y)', 'Union(x, y) 是否回傳最大值'], 'Find(x) 是否等於 Find(y)', '若 Find(x) 與 Find(y) 回傳的代表相同，代表 x 與 y 屬於同一集合。', True, 'medium'), ('Kruskal 最小生成樹演算法中，不相交集合主要用來做什麼？', ['儲存所有邊的權重', '將邊依權重排序', '計算最短路徑', '判斷加入邊時是否形成 cycle'], '判斷加入邊時是否形成 cycle', 'Kruskal 演算法中，不相交集合可用來判斷兩個頂點是否已連通，避免加入邊後形成 cycle。', True, 'hard'), ('Make-Set(x) 的功能為何？', ['建立只包含 x 的新集合', '將 x 從集合中刪除', '找出 x 的左右子樹', '將 x 加入優先佇列'], '建立只包含 x 的新集合', 'Make-Set(x) 會建立一個只包含 x 的集合，並讓 x 自己成為該集合的代表。', True, 'easy'), ('若同時使用路徑壓縮與依秩合併，Disjoint Set 多次操作的均攤時間複雜度通常可表示為何？', ['O(n^2)', 'O(log n)', 'O(α(n))，其中 α 為反 Ackermann 函數', 'O(n!)'], 'O(α(n))，其中 α 為反 Ackermann 函數', '路徑壓縮搭配 Union by Rank 或 Size 時，多次操作均攤時間非常接近常數，通常表示為 O(α(n))。', True, 'hard'), ('執行 Union(x, y) 時，如果 x 與 y 已經在同一集合中，通常應該如何處理？', ['強制建立新集合', '刪除其中一個元素', '不需要再合併，保持原狀', '將所有元素排序'], '不需要再合併，保持原狀', 'Union 通常會先檢查兩個元素代表是否相同，若已相同，不需要再合併。', True, 'medium'), ('使用不相交集合求無向圖連通元時，通常會對每一條邊 (u, v) 做什麼？', ['將 u 與 v 放入堆疊', '對 u 與 v 執行 Union', '對所有點執行排序', '刪除權重最大的邊'], '對 u 與 v 執行 Union', '處理無向圖連通元時，通常遍歷每條邊，並對邊的兩個端點執行 Union。', True, 'medium')]

        Question.objects.all().delete()

        for text, options_list, answer, explanation, is_original, difficulty in data:
            question = Question.objects.create(
                chapter=9,
                text=text,
                explanation=explanation,
                is_original=is_original,
                difficulty=difficulty,
            )

            for option_text in options_list:
                Choice.objects.create(
                    question=question,
                    text=option_text,
                    is_correct=(option_text == answer),
                )

        self.stdout.write(self.style.SUCCESS(f'已匯入 {len(data)} 題題目。'))
