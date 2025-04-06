import React from 'react';
import { useNavigate } from 'react-router-dom';
import poster from '../assets/poster.jpg';
import './MovieCard.css';

const GENRES = [
  'unknown', 'Action', 'Adventure', 'Animation', "Children's", 'Comedy', 'Crime', 'Documentary',
  'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western'
];

function MovieCard({ movie }) {
  const navigate = useNavigate();

  const filledStars = Math.round(movie.rating / 2); // Convert 10-point rating to 5 stars
  const stars = Array(5)
    .fill('★', 0, filledStars)
    .fill('☆', filledStars);

  // Convert integer to binary array of bits
  const genreBits = movie.genres
    .toString(2)
    .padStart(19, '0')
    .split('')
    .map(Number);

  const genreTags = genreBits
    .map((bit, idx) => (bit === 1 ? GENRES[idx] : null))
    .filter(Boolean);

  return (
    <div className="movie-card" onClick={() => navigate(`/movie/${movie.id}`)}>
      <img src={poster} alt={movie.title} className="movie-img" />
      <div className="movie-info">
        <div className="title">{movie.title}</div>
        <div className='date'>{movie.date}</div>
        <div className="rating">
          评分: {movie.rating} <span className="stars">{stars.join('')}</span>
        </div>
        <div className="genres">
          {genreTags.map(tag => (
            <span className="genre-tag" key={tag}>{tag}</span>
          ))}
        </div>
      </div>
    </div>
  );
}

export default MovieCard;