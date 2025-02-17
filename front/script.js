document.addEventListener('DOMContentLoaded', () => {
    // 目標達成の条件をチェックする関数
    function checkGoalAchieved() {
        // ここに目標達成の条件を記述
        // 例: 目標達成のフラグがtrueの場合
        const goalAchieved = true; // これは例です。実際の条件に置き換えてください。

        if (goalAchieved) {
            displaySticker();
            displayMessage();
        }
    }

    // ステッカーを表示する関数
    function displaySticker() {
        const sticker = document.getElementById('sticker');
        if (sticker) {
            sticker.style.display = 'block';
        }
    }

    // メッセージを表示する関数
    function displayMessage() {
        const message = document.createElement('div');
        message.textContent = '目標達成おめでとうございます！';
        message.style.fontSize = '20px';
        message.style.color = 'green';
        document.body.appendChild(message);
    }

    // 目標達成のチェックを実行
    checkGoalAchieved();
});