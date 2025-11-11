(function () {
  function initCK5() {
    document.querySelectorAll('textarea.ckeditor5').forEach(function (ta) {
      if (ta._ck5_inited) return;
      ta._ck5_inited = true;

      ClassicEditor.create(ta, {
        toolbar: [
          'heading', '|',
          'bold', 'italic', 'underline', 'link',
          'bulletedList', 'numberedList', 'blockQuote',
          'insertTable', 'undo', 'redo'
        ],
        language: 'vi'
      }).then(function (editor) {
        var form = ta.closest('form');
        if (form && !form._ck5_bound) {
          form._ck5_bound = true;
          form.addEventListener('submit', function () {
            document.querySelectorAll('textarea.ckeditor5').forEach(function (t) {
              if (t._ck5_editor && t._ck5_editor.getData) {
                t.value = t._ck5_editor.getData();
              }
            });
          });
        }
        ta._ck5_editor = editor;
      }).catch(console.error);
    });
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initCK5);
  } else {
    initCK5();
  }
})();
