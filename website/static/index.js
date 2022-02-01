/*
 * @Date: 2021-10-30 20:46:21
 * @LastEditors: GC
 * @LastEditTime: 2021-11-02 15:19:28
 * @FilePath: \Flask-Project\website\static\index.js
 */


function deleteNote(noteId) {
    fetch("/delete-note", {
        method: "POST",
        body: JSON.stringify({ noteId: noteId }),
    }).then((_res) => {
        // Reload the window
        window.location.href = "/";
    });
}