const request = indexedDB.open('train-db', 1);

request.onsuccess = (event) => {
  const db = event.target.result;
  const tx = db.transaction('delays', 'readonly');
  const store = tx.objectStore('delays');
  const getAll = store.getAll();

  getAll.onsuccess = () => {
    renderTimetable(getAll.result);
  };
};