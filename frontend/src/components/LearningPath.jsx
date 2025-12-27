// import React, { useEffect, useState } from "react";

// const LearningPath = () => {
//   const [data, setData] = useState(null);

//   useEffect(() => {
//     fetch("http://127.0.0.1:8000/api/agent/learning_path/student_123")
//       .then((res) => res.json())
//       .then((json) => setData(json))
//       .catch((err) => console.error(err));
//   }, []);

//   if (!data)
//     return (
//       <div className="flex justify-center items-center min-h-screen text-white">
//         Loading...
//       </div>
//     );

//   return (
//     <div className="min-h-screen bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 p-6 text-white">
//       <div className="max-w-3xl mx-auto bg-white/20 backdrop-blur-md p-8 rounded-3xl border border-white/30">
//         <h1 className="text-3xl font-bold mb-4">📚 Personalized Learning Path</h1>

//         <pre className="bg-black/30 p-4 rounded-xl overflow-auto">
//           {JSON.stringify(data, null, 2)}
//         </pre>
//       </div>
//     </div>
//   );
// };

// export default LearningPath;


import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

const LearningPath = () => {
  const navigate = useNavigate();
  const [pathData, setPathData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const extractValidJSON = (input) => {
    if (!input) return null;

    try {
      // Case 1: Already object
      if (typeof input === "object") return input;

      // Case 2: Extract inside string
      const match = input.match(/\{[\s\S]*\}/);
      if (match) return JSON.parse(match[0]);
    } catch {
      return null;
    }

    return null;
  };

  useEffect(() => {
    const loadData = async () => {
      try {
        const res = await fetch(
          "http://127.0.0.1:8000/api/agent/learning_path/student_123"
        );

        const data = await res.json();
        console.log("🔥 RAW LEARNING PATH:", data);

        if (!data.learning_path) {
          setError("No learning path found.");
          setLoading(false);
          return;
        }

        let lp = data.learning_path;
        let parsed = extractValidJSON(lp);

        if (!parsed) {
          setError("Learning path format invalid.");
          setLoading(false);
          return;
        }

        setPathData(parsed);
      } catch (err) {
        console.error("🔥 FETCH ERROR:", err);
        setError("Unable to load learning path.");
      }

      setLoading(false);
    };

    loadData();
  }, []);

  // Loading Screen
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center text-white text-2xl">
        ⏳ Loading Learning Path...
      </div>
    );
  }

  // Error screen OR empty fallback
  if (
    error ||
    !pathData ||
    !Array.isArray(pathData.learning_path) ||
    pathData.learning_path.length === 0
  ) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center text-white text-3xl bg-gradient-to-br from-purple-600 to-pink-600">
        ⚠️ {error || pathData?.summary || "Learning path format invalid."}
        <button
          onClick={() => navigate("/evaluation")}
          className="mt-6 bg-white text-indigo-700 px-6 py-3 rounded-xl font-semibold hover:bg-gray-100 transition"
        >
          Go Back
        </button>
      </div>
    );
  }

  // Main UI
  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-600 to-indigo-600 p-10 text-white">
      <h1 className="text-4xl font-extrabold mb-10">
        📚 Personalized Learning Path
      </h1>

      {pathData.learning_path.map((item, i) => (
        <div
          key={i}
          className="bg-white/20 backdrop-blur-md p-6 rounded-2xl border border-white/30 mb-6 shadow-xl"
        >
          <h2 className="text-2xl font-semibold text-yellow-300 mb-2">
            {i + 1}. {item.topic}
          </h2>

          <p className="text-gray-200 mb-4">{item.why_important}</p>

          <h3 className="text-xl font-semibold text-green-300 mb-2">📌 Subtopics</h3>
          <ul className="list-disc ml-6 text-gray-100 mb-4">
            {item.subtopics?.map((s, idx) => (
              <li key={idx}>{s}</li>
            ))}
          </ul>

          <h3 className="text-xl font-semibold text-blue-300 mb-2">🔗 Resources</h3>
          <ul className="list-disc ml-6 text-gray-100 mb-4">
            {item.resources?.map((r, idx) => (
              <li key={idx}>
                <a
                  href={r.link}
                  target="_blank"
                  rel="noreferrer"
                  className="underline text-white hover:text-yellow-200"
                >
                  {r.title}
                </a>
              </li>
            ))}
          </ul>

          <h3 className="text-xl font-semibold text-pink-300 mb-2">
            📝 Practice Tasks
          </h3>
          {item.practice_tasks?.map((task, idx) => (
            <div
              key={idx}
              className="bg-white/10 p-4 rounded-xl border border-white/20 mb-3"
            >
              <p className="font-semibold text-white mb-1">{task.question}</p>

              <ul className="list-disc ml-6 text-gray-200">
                {task.options?.map((opt, j) => (
                  <li key={j}>{opt}</li>
                ))}
              </ul>

              <p className="text-green-300 mt-1">
                ✔ Correct: <span className="text-white">{task.correct}</span>
              </p>
            </div>
          ))}
        </div>
      ))}

      <div className="bg-white/10 p-6 rounded-xl border border-white/20 mt-8">
        <h2 className="text-2xl font-semibold text-orange-300 mb-2">📘 Summary</h2>
        <p className="text-gray-200">{pathData.summary}</p>
      </div>

      <div className="text-center mt-10">
        <button
          onClick={() => navigate("/evaluation")}
          className="bg-white text-blue-700 px-6 py-3 rounded-xl font-semibold hover:bg-gray-100 transition"
        >
          📑 Other Agents
        </button>
      </div>
    </div>
  );
};

export default LearningPath;
