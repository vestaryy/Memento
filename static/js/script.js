document.addEventListener('DOMContentLoaded', function() {
    const toggleBtn = document.getElementById('toggleArchive');
    if (toggleBtn) {
        toggleBtn.addEventListener('click', function() {
            const hiddenItems = document.querySelectorAll('.memory-item.d-none');
            const allItems = document.querySelectorAll('.memory-item');
            
            if (hiddenItems.length > 0) {
                hiddenItems.forEach(item => item.classList.remove('d-none'));
                this.innerText = 'Скрыть архив';
            } else {
                allItems.forEach((item, index) => { if (index >= 3) item.classList.add('d-none'); });
                this.innerText = 'Показать весь архив';
            }
        });
    }
});

function openCapsule() {
    const gridItems = document.querySelectorAll('.memory-item');
    const slidesContainer = document.getElementById('capsuleSlides');
    const summaryText = document.getElementById('summaryText');
    slidesContainer.innerHTML = '';
    
    let descriptions = [];

    gridItems.forEach((item, index) => {
        const img = item.querySelector('img').src;
        const text = item.querySelector('.memory-text').innerText;
        descriptions.push(text.toLowerCase());

        const activeClass = index === 0 ? 'active' : '';
        slidesContainer.innerHTML += `
            <div class="carousel-item ${activeClass}">
                <img src="${img}" class="d-block mx-auto shadow-lg">
            </div>`;
    });

    document.getElementById('capsuleOverlay').classList.remove('d-none');

    const actions = descriptions.join(' ').match(/[а-яА-Я]+(ли|ла|ло|ли|ал|ял)\b/g) || ["проживали"];
    const uniqueActions = [...new Set(actions)].slice(0, 2).join(" и ");
    const worries = ["грустно", "сложно", "переживал", "трудно", "устал", "проблема"];
    const hasWorry = descriptions.some(desc => worries.some(w => desc.includes(w)));

    let response = `В последнее время вы часто <b>${uniqueActions}</b>. `;
    if (hasWorry) {
        response += `Также вы переживали по некоторым поводам, но всё наладилось, ведь моменты счастья всегда возвращаются!`;
    } else {
        response += `Судя по кадрам, вы старались ценить каждое мгновение.`;
    }

    summaryText.innerHTML = "<i>Анализирую ваши воспоминания...</i>";
    setTimeout(() => { summaryText.innerHTML = response; }, 1200);
}

function closeCapsule() {
    document.getElementById('capsuleOverlay').classList.add('d-none');
}
