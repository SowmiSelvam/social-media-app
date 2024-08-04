import React, { useState, useEffect } from 'react';
import { getUserNotes, addNote, updateNote, deleteNote } from '../services/api';

const Profile = () => {
  const [notes, setNotes] = useState([]);
  const [newNoteContent, setNewNoteContent] = useState('');
  const [editedNoteContent, setEditedNoteContent] = useState('');
  const [updatingNoteId, setUpdatingNoteId] = useState(null);
  const [error, setError] = useState('');


  useEffect(() => {
    const fetchUserNotes = async () => {
      try {
        const data = await getUserNotes();
        setNotes(data);
      } catch (error) {
        console.error('Error fetching user notes:', error);
      }
    };

    fetchUserNotes();
  }, []);

  const handleAddNote = async () => {
    try {
      const response = await addNote({ content: newNoteContent });
      setNotes([...notes, response.notes]); 
      setNewNoteContent('');
    } catch (error) {
      setError(error.error);
    }
  };

  const handleDeleteNote = async (noteId) => {
    try {
      await deleteNote(noteId);
      setNotes(notes.filter(note => note.id !== noteId));
    } catch (error) {
      console.error('Error deleting note:', error);
    }
  };

  const handleUpdateNote = async (noteId) => {
    try {
      const updatedNote = await updateNote(noteId, { content: editedNoteContent });
      console.log('Update note response:', updatedNote);

      if (updatedNote) {
        setNotes(notes.map(note =>
          note.id === noteId ? { ...note, content: editedNoteContent } : note
        ));
        setUpdatingNoteId(null);
        setEditedNoteContent('');
      }
    } catch (error) {
      console.error('Error updating note:', error);
    }
  };

  return (
    <div className="container mt-4">
      <h2 className="mb-4">My Posts</h2>
      <div className="card">
        <div className="card-body">
          <h3 className="card-title">My Notes:</h3>
          <ul className="list-group">
            {notes.map((note) => (
              <li key={note.id} className="list-group-item">
                {updatingNoteId === note.id ? (
                  <div>
                    <textarea
                      className="form-control mb-2"
                      value={editedNoteContent}
                      onChange={(e) => setEditedNoteContent(e.target.value)}
                    />
                    <button className="btn btn-sm btn-primary mx-1" onClick={() => handleUpdateNote(note.id)}>Save</button>
                    <button className="btn btn-sm btn-outline-secondary mx-1" onClick={() => setUpdatingNoteId(null)}>Cancel</button>
                  </div>
                ) : (
                  <>
                    {note.content}
                    <button className="btn btn-sm btn-outline-primary mx-1" onClick={() => { setUpdatingNoteId(note.id); setEditedNoteContent(note.content); }}>Edit</button>
                    <button className="btn btn-sm btn-outline-danger mx-1" onClick={() => handleDeleteNote(note.id)}>Delete</button>
                  </>
                )}
              </li>
            ))}
          </ul>
        </div>
      </div>

      <div className="mt-3 mb-3">
      {error && <p className="text-danger">{error}</p>}
        <textarea
          className="form-control"
          rows="3"
          placeholder="Enter new note"
          value={newNoteContent}
          onChange={(e) => setNewNoteContent(e.target.value)}
        />
        <button className="btn btn-primary mt-2" onClick={handleAddNote}>Add Note</button>
      </div>
    </div>
  );
};

export default Profile;
