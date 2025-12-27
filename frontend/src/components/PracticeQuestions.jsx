// import React, { useEffect, useState } from "react";

// const PracticeQuestions = () => {
//   const [data, setData] = useState(null);

//   useEffect(() => {
//     fetch("http://127.0.0.1:8000/api/agent/practice_questions/student_123?num_questions=5")
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
//         <h1 className="text-3xl font-bold mb-4">✏ Practice Questions</h1>

//         <pre className="bg-black/30 p-4 rounded-xl overflow-auto">
//           {JSON.stringify(data, null, 2)}
//         </pre>
//       </div>
//     </div>
//   );
// };

// export default PracticeQuestions;


import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

const PracticeQuestions = () => {
  const navigate = useNavigate();

  const [loading, setLoading] = useState(true);
  const [practice, setPractice] = useState(null);
  const [numQuestions, setNumQuestions] = useState(5);
  const [error, setError] = useState(null);

  const fetchQuestions = async () => {
    setLoading(true);
    setError(null);

    try {
      const res = await fetch(
        `http://127.0.0.1:8000/api/agent/practice_questions/student_123?num_questions=${numQuestions}`
      );

      const raw = await res.json();
      console.log("🔥 RAW PRACTICE RESPONSE:", raw);

      // Support ANY valid backend field
      let output =
        raw.practice_questions ||
        raw.questions_json ||
        raw.questions ||
        raw.analysis ||
        raw.practice ||
        null;

      if (!output) {
        setError("No practice questions found.");
        setLoading(false);
        return;
      }

      // Convert object → JSON string if needed
      if (typeof output === "object") {
        setPractice(output.practice_questions);
        setLoading(false);
        return;
      }

      // Clean ```json wrappers
      output = output.replace(/```json/gi, "").replace(/```/g, "").trim();

      let parsed;
      try {
        parsed = JSON.parse(output);
      } catch (err) {
        console.error("❌ PARSE ERROR:", err);
        setError("Failed to parse questions JSON.");
        setLoading(false);
        return;
      }

      if (!parsed.practice_questions) {
        setError("Invalid practice questions format.");
        setLoading(false);
        return;
      }

      setPractice(parsed.practice_questions);
    } catch (err) {
      console.error("🔥 Fetch error:", err);
      setError("Network or server error.");
    }

    setLoading(false);
  };

  // Load on page open
  useEffect(() => {
    fetchQuestions();
  }, []);

  // Loading screen
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center text-white text-3xl">
        ⏳ Loading Practice Questions...
      </div>
    );
  }

  // Error screen
  if (error) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-purple-600 to-pink-600 text-white text-3xl">
        ⚠️ {error}
        <button
          onClick={() => navigate("/evaluation")}
          className="mt-6 bg-white text-indigo-700 px-6 py-3 rounded-xl font-semibold hover:bg-gray-100 transition"
        >
          Go Back
        </button>
      </div>
    );
  }

  // MAIN UI
  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-600 to-indigo-600 p-10 text-white">
      <h1 className="text-4xl font-extrabold mb-10">✏ Practice Questions</h1>

      {/* Input box */}
      <div className="mb-8 flex items-center gap-4">
        <input
          type="number"
          min="1"
          max="20"
          value={numQuestions}
          onChange={(e) => setNumQuestions(e.target.value)}
          className="p-3 rounded-xl text-black w-28"
        />

        <button
          onClick={fetchQuestions}
          className="bg-white text-purple-700 px-6 py-3 rounded-xl font-semibold hover:bg-gray-100 transition"
        >
          Generate
        </button>
      </div>

      {/* Display all questions */}
      <div className="space-y-6">
        {practice?.map((q, i) => (
          <div
            key={i}
            className="bg-white/20 backdrop-blur-md p-6 rounded-2xl border border-white/30 shadow-xl"
          >
            <h2 className="text-xl font-semibold text-yellow-300 mb-3">
              {i + 1}. {q.question}
            </h2>

            <ul className="list-disc ml-6 text-gray-200 mb-3">
              {q.options.map((opt, idx) => (
                <li key={idx}>{opt}</li>
              ))}
            </ul>

            <p className="text-green-300">
              ✔ Correct: <span className="text-white">{q.correct_answer}</span>
            </p>

            <p className="text-blue-200 mt-2">💡 {q.explanation}</p>
          </div>
        ))}
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

export default PracticeQuestions;
