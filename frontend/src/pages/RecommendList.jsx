import { useState, useEffect } from 'react';
import MovieCard from '../components/MovieCard';

function RecommendList() {
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchTopK = async () => {
      setLoading(true);
      try {
        // 这里添加获取 TopK 推荐的 API 调用
        // const response = await fetch('your-api-endpoint');
        // const data = await response.json();
        // setRecommendations(data);
        
        // 临时模拟数据
        setRecommendations([
          { 
            id: 1, 
            title: "The Shawshank Redemption", 
            year: 1994,
            release_date: "1994-09-23",
            imdb_url: "https://www.imdb.com/title/tt0111161/",
            rating: 9.3,
            genres: [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
          },
          { 
            id: 2, 
            title: "The Godfather", 
            year: 1972,
            release_date: "1972-03-24",
            imdb_url: "https://www.imdb.com/title/tt0068646/",
            rating: 9.2,
            genres: [0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
          },
          { 
            id: 3, 
            title: "The Dark Knight", 
            year: 2008,
            release_date: "2008-07-18",
            imdb_url: "https://www.imdb.com/title/tt0468569/",
            rating: 9.0,
            genres: [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
          },
        ]);
      } catch (error) {
        console.error('Error fetching recommendations:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchTopK();
  }, []);

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-2xl sm:text-3xl font-bold mb-6 sm:mb-8">🏆 Top Recommended Movies</h1>
      
      {loading ? (
        <div className="flex justify-center items-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900"></div>
        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-4 sm:gap-6">
          {recommendations.map((movie) => (
            <MovieCard key={movie.id} movie={movie} />
          ))}
        </div>
      )}
    </div>
  );
}

export default RecommendList;