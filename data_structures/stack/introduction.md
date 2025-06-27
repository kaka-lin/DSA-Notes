# Stack 介紹

> the newest element added to the queue will be processed first

## 基本概念

Stack (堆疊) 是一種 `Last-In-First-Out (LIFO)` 的資料結構。這意味著最後被加入的元素，將會是第一個被移除的。可以想像成一疊盤子，你總是從最上面放上新盤子，也從最上面拿走盤子。

### 常見操作

- **Push**: 將一個元素放到堆疊的最頂端。
- **Pop**: 移除並回傳堆疊最頂端的元素。
- **Peek / Top**: 回傳堆疊最頂端的元素，但不將其移除。
- **isEmpty**: 檢查堆疊是否為空。

## 應用場景

- 函式呼叫 (Call Stack)
- 表達式求值 (例如：中序轉後序)
- 語法解析 (Parsing)
- 瀏覽器的上一頁功能
- 深度優先搜尋 (DFS)
