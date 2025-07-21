import React, { useState, useRef, useEffect } from 'react';
import './App.css';
import API from '../API.js'

const difficultyOptions = ['Easy', 'Medium', 'Hard'];
const topicOptions = [
  "Array",
  "String",
  "Linked List",
  "Tree",
  "Binary Tree",
  "Binary Search Tree",
  "Graph",
  "DFS",
  "BFS",
  "Dynamic Programming",
  "Backtracking",
  "Greedy",
  "Sorting",
  "Hash Table",
  "Stack",
  "Queue",
  "Heap / Priority Queue",
  "Two Pointers",
  "Sliding Window",
  "Recursion",
  "Bit Manipulation",
  "Math / Number Theory",
  "Design",
  "Trie",
  "Union Find / Disjoint Set",
];

export default function App() {
  const [difficulties, setDifficulties] = useState([]);
  const [topics, setTopics] = useState([]);
  const [chatInput, setChatInput] = useState('');

  const [date, setDate] = useState('');
  const [time, setTime] = useState('');

  const [showDifficulty, setShowDifficulty] = useState(false);
  const [showTopics, setShowTopics] = useState(false);

  const diffRef = useRef(null);
  const topicRef = useRef(null);

  async function handleSubmit(e) {
    e.preventDefault();

    alert(`Submitted:
    Difficulties: ${difficulties.join(', ') || 'None'}
    Topics: ${topics.join(', ') || 'None'}
    Chat: ${chatInput || '(empty)'}
    YouTube Date: ${date || 'Not set'}
    YouTube Time: ${time || 'Not set'}`);
    
    const payload = {
      'input' : chatInput,
      'topics' : topics,
      'difficulty' : difficulties,
      'date' : date,
      'time' : time
    }

    const response = await API.scheduleStream(payload);

    if (response.ok) {
      const data = await response.json();

      console.log(data);
    } else {
      console.error('Encountered error');
    }
  }

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (diffRef.current && !diffRef.current.contains(event.target)) {
        setShowDifficulty(false);
      }
      if (topicRef.current && !topicRef.current.contains(event.target)) {
        setShowTopics(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const toggleSelection = (value, current, setter) => {
    setter(current.includes(value) ? current.filter(v => v !== value) : [...current, value]);
  };

//   const handleSubmit = () => {
//     alert(`Submitted:
// Difficulties: ${difficulties.join(', ') || 'None'}
// Topics: ${topics.join(', ') || 'None'}
// Chat: ${chatInput || '(empty)'}
// YouTube Date: ${date || 'Not set'}
// YouTube Time: ${time || 'Not set'}`);
//   };

  return (
    <div className="container">
      <h1>LeetCode Stream Setup</h1>

      {/* LeetCode Section */}
      <h2 className="subheader">LeetCode:</h2>

      <div className="dropdown-group">
        {/* Difficulty Dropdown */}
        <div className="dropdown" ref={diffRef}>
          <button
            className="dropdown-btn"
            onClick={() => setShowDifficulty(prev => !prev)}
            type="button"
            aria-expanded={showDifficulty}
          >
            Difficulty: {difficulties.length > 0 ? difficulties.join(', ') : 'Select'}
          </button>
          <div className={`dropdown-content ${showDifficulty ? 'show' : ''}`}>
            {difficultyOptions.map((option) => (
              <label key={option} className={`difficulty-label difficulty-${option.toLowerCase()}`}>
                <input
                  type="checkbox"
                  value={option}
                  checked={difficulties.includes(option)}
                  onChange={() => toggleSelection(option, difficulties, setDifficulties)}
                />
                <span>{option}</span>
              </label>
            ))}
          </div>
        </div>

        {/* Topics Dropdown */}
        <div className="dropdown" ref={topicRef}>
          <button
            className="dropdown-btn"
            onClick={() => setShowTopics(prev => !prev)}
            type="button"
            aria-expanded={showTopics}
          >
            Topics: {topics.length > 0 ? topics.join(', ') : 'Select'}
          </button>
          <div className={`dropdown-content ${showTopics ? 'show' : ''}`}>
            {topicOptions.map((option) => (
              <label key={option}>
                <input
                  type="checkbox"
                  value={option}
                  checked={topics.includes(option)}
                  onChange={() => toggleSelection(option, topics, setTopics)}
                />
                <span>{option}</span>
              </label>
            ))}
          </div>
        </div>
      </div>

      <textarea
        className="chatbox"
        placeholder="What kind of problem would you like to solve?"
        value={chatInput}
        onChange={(e) => setChatInput(e.target.value)}
      />

      {/* YouTube Section */}
      <h2 className="subheader">YouTube:</h2>

      <label htmlFor="stream-date" className="input-label">Stream Date:</label>
      <input
        id="stream-date"
        type="date"
        value={date}
        onChange={(e) => setDate(e.target.value)}
        className="input-field"
      />

      <label htmlFor="stream-time" className="input-label">Stream Time:</label>
      <input
        id="stream-time"
        type="time"
        step="1"
        value={time}
        onChange={(e) => setTime(e.target.value)}
        className="input-field"
      />

      <button className="submit-btn" onClick={handleSubmit} type="button">
        Submit
      </button>
    </div>
  );
}