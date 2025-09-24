(() => {
  const image = document.getElementById('sourceImage');
  const stage = document.getElementById('imageStage');
  const selection = document.getElementById('selection');
  const info = document.getElementById('info');
  const resetBtn = document.getElementById('resetBtn');

  let isSelecting = false;
  let startX = 0;
  let startY = 0;
  let currentX = 0;
  let currentY = 0;

  function pointerToStageCoords(evt) {
    const rect = stage.getBoundingClientRect();
    const clientX = evt.touches ? evt.touches[0].clientX : evt.clientX;
    const clientY = evt.touches ? evt.touches[0].clientY : evt.clientY;
    const x = Math.max(0, Math.min(clientX - rect.left, rect.width));
    const y = Math.max(0, Math.min(clientY - rect.top, rect.height));
    return { x, y };
  }

  function updateSelection() {
    const left = Math.min(startX, currentX);
    const top = Math.min(startY, currentY);
    const width = Math.abs(currentX - startX);
    const height = Math.abs(currentY - startY);

    if (width < 2 || height < 2) {
      selection.classList.add('hidden');
      info.textContent = '';
      return;
    }

    selection.classList.remove('hidden');
    selection.style.left = left + 'px';
    selection.style.top = top + 'px';
    selection.style.width = width + 'px';
    selection.style.height = height + 'px';

    info.textContent = `x:${Math.round(left)}, y:${Math.round(top)}, w:${Math.round(width)}, h:${Math.round(height)}`;
  }

  function onPointerDown(evt) {
    evt.preventDefault();
    const p = pointerToStageCoords(evt);
    isSelecting = true;
    startX = currentX = p.x;
    startY = currentY = p.y;
    updateSelection();
  }

  function onPointerMove(evt) {
    if (!isSelecting) return;
    const p = pointerToStageCoords(evt);
    currentX = p.x;
    currentY = p.y;
    updateSelection();
  }

  function onPointerUp() {
    isSelecting = false;
  }

  function resetSelection() {
    selection.classList.add('hidden');
    selection.style.width = '0px';
    selection.style.height = '0px';
    info.textContent = '';
  }

  // Привязываем обработчики к сцене, чтобы работать по всей области изображения
  stage.addEventListener('mousedown', onPointerDown);
  window.addEventListener('mousemove', onPointerMove);
  window.addEventListener('mouseup', onPointerUp);

  stage.addEventListener('touchstart', onPointerDown, { passive: false });
  window.addEventListener('touchmove', onPointerMove, { passive: false });
  window.addEventListener('touchend', onPointerUp);

  resetBtn.addEventListener('click', resetSelection);

  // Убедимся, что размер selection сбрасывается при ресайзе
  window.addEventListener('resize', resetSelection);

  // Если картинка ещё не прогружена, сбрасываем после загрузки для корректного bbox
  if (!image.complete) {
    image.addEventListener('load', resetSelection);
  }
})();


