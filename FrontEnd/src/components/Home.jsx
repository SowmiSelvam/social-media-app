import React, { useEffect, useState } from 'react';
import { fetchAllNotes } from '../services/api';  

const Home = () => {
  const [notes, setNotes] = useState([]);

  useEffect(() => {
    const getNotes = async () => {
      try {
        const data = await fetchAllNotes();
        console.log(data);
        setNotes(data.notes);
      } catch (error) {
        console.error('Error fetching notes:', error);
      }
    };

    getNotes();
  }, []);

  return (
    <div className="container mt-4">
      <h2>Posts</h2>
     
        <ul className="list-group">
          {notes.map((note) => (
            <li key={note.id} className="list-group-item">
              <p className='font-weight-bold' >{note.username}</p>
             <p>{note.content}</p>
              </li>
          ))}
        </ul>

    </div>
  );
};

export default Home;
