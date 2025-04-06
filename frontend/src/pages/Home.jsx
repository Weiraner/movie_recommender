import React, { useState, useEffect } from 'react';
import MovieCard from '../components/MovieCard';
import './Home.css';

function Home() {
  const [movies, setMovies] = useState([]);
  const [keyword, setKeyword] = useState('');
  const userId = 1; // 假设用户ID为1，实际应用中应该从用户登录状态获取

  // get recommend movies
  const fetchRecommendations = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/recommend', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ user_id: userId })
      });
      
      if (!response.ok) {
        throw new Error('Failed to fetch recommendations');
      }
      
      const data = await response.json();
      console.log('Raw response:', data.top_k);
      setMovies(data.top_k);
    } catch (error) {
      console.error('Error fetching recommendations:', error);
    }
  };

  useEffect(() => {
    fetchRecommendations();
  }, []);
// useEffect(() => {
//     setMovies([
//       { 
//         id: 1, 
//         title: "The Shawshank Redemption", 
//         year: 1994,
//         release_date: "1994-09-23",
//         imdb_url: "https://www.imdb.com/title/tt0111161/",
//         rating: 9.3,
//         genres: 11
//       },
//       { 
//         id: 2, 
//         title: "The Godfather", 
//         year: 1972,
//         release_date: "1972-03-24",
//         imdb_url: "https://www.imdb.com/title/tt0068646/",
//         rating: 9.2,
//         genres: 19
//       },
//       { 
//         id: 3, 
//         title: "The Dark Knight", 
//         year: 2008,
//         release_date: "2008-07-18",
//         imdb_url: "https://www.imdb.com/title/tt0468569/",
//         rating: 9.0,
//         genres: 77
//       },
//     ]);
//   }, []);  

const filteredMovies = movies.filter(m => m.title.includes(keyword));
// const filteredMovies = movies;
return (
    <div className="container">
      <input
        type="text"
        placeholder="搜索关键词"
        value={keyword}
        onChange={(e) => setKeyword(e.target.value)}
        className="search-bar"
      />
      <div className="recommend-list">
        {filteredMovies.map(movie => (
          <div className="card-wrapper" key={movie.id}>
            <MovieCard movie={movie} />
          </div>
        ))}
      </div>
    </div>
  );
}

export default Home;