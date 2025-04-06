import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';

function MovieDetail() {
  const { id } = useParams();
  const [movie, setMovie] = useState(null);

  useEffect(() => {
    fetch(`/api/movie/${id}`) // replace with your API
      .then(res => res.json())
      .then(data => setMovie(data));
  }, [id]);

  if (!movie) return <div>加载中...</div>;

  return (
    <div style={{ padding: '16px' }}>
      <h1>{movie.title} ({movie.year})</h1>
      <img src={movie.cover} alt={movie.title} style={{ maxWidth: '300px' }} />
      <p>评分: {movie.rating}</p>
      <p>类型: {movie.genre}</p>
      <p>{movie.description}</p>
    </div>
  );
}

export default MovieDetail;