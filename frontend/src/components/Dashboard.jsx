import React from "react";
import { useNavigate } from "react-router-dom";

const Dashboard = () => {
  const navigate = useNavigate();

  const cards = [
    { title: "Weak Concepts", route: "/agent/weak", emoji: "🔍" },
    { title: "Learning Path", route: "/agent/learning-path", emoji: "📚" },
    { title: "Exam Readiness", route: "/agent/exam-readiness", emoji: "📊" },
    { title: "Practice Questions", route: "/agent/practice-questions", emoji: "📝" },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-500 to-pink-500 p-10 text-white">
      <h1 className="text-4xl font-bold mb-8 text-center">
        🎯 Student Analysis Dashboard
      </h1>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 max-w-5xl mx-auto">
        {cards.map((c, i) => (
          <div
            key={i}
            onClick={() => navigate(c.route)}
            className="bg-white/20 hover:bg-white/30 backdrop-blur-md rounded-2xl 
                       p-6 border border-white/30 cursor-pointer transition 
                       transform hover:scale-[1.03] shadow-xl"
          >
            <h2 className="text-2xl font-semibold">
              {c.emoji} {c.title}
            </h2>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Dashboard;
