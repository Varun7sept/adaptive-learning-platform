// import React, { useEffect, useState } from "react";
// import { useNavigate } from "react-router-dom";

// const WeakConcepts = () => {
//   const navigate = useNavigate();
//   const studentId = "student_123"; // you can make dynamic later

//   const [loading, setLoading] = useState(true);
//   const [analysis, setAnalysis] = useState(null);

//   useEffect(() => {
//     const fetchWeakConcepts = async () => {
//       try {
//         const res = await fetch(
//           `http://127.0.0.1:8000/api/agent/weak_concepts/${studentId}`
//         );
//         const data = await res.json();

//         // Parse JSON string coming from backend
//         let parsed = null;
//         try {
//           parsed = JSON.parse(data.agent_analysis);
//         } catch {
//           parsed = data.agent_analysis;
//         }

//         setAnalysis(parsed);
//       } catch (err) {
//         console.error(err);
//       }
//       setLoading(false);
//     };

//     fetchWeakConcepts();
//   }, []);

//   if (loading) {
//     return (
//       <div className="min-h-screen flex items-center justify-center text-white text-2xl">
//         ⏳ Loading...
//       </div>
//     );
//   }

//   return (
//     <div className="min-h-screen bg-gradient-to-br from-purple-500 to-indigo-600 p-10 text-white">
//       <h1 className="text-4xl font-bold mb-6">🔍 Weak Concepts</h1>

//       {/* Concepts List */}
//       <div className="space-y-4">
//         {analysis?.weak_concepts?.map((item, i) => (
//           <div
//             key={i}
//             className="bg-white/20 backdrop-blur-md rounded-xl p-5 border border-white/30 shadow-lg"
//           >
//             <h3 className="text-xl font-semibold text-yellow-300 mb-2">
//               {i + 1}. {item.concept}
//             </h3>
//             <p className="text-gray-200">{item.why_weak}</p>
//           </div>
//         ))}
//       </div>

//       {/* Summary Card */}
//       <div className="mt-8 bg-white/10 p-5 rounded-xl border border-white/20 backdrop-blur-md">
//         <h2 className="text-2xl font-semibold mb-2 text-green-300">📌 Summary</h2>
//         <p className="text-gray-200">{analysis?.summary}</p>
//       </div>

//       <div className="text-center mt-8">
//         <button
//           onClick={() => navigate("/")}
//           className="bg-white text-indigo-600 px-6 py-3 rounded-xl font-semibold hover:bg-gray-100 transition-all"
//         >
//           Back to Dashboard
//         </button>
//       </div>
//     </div>
//   );
// };

// export default WeakConcepts;


// import React, { useEffect, useState } from "react";
// import { useNavigate } from "react-router-dom";

// const WeakConcepts = () => {
//   const navigate = useNavigate();
//   const studentId = "student_123"; // later can be dynamic

//   const [loading, setLoading] = useState(true);
//   const [analysis, setAnalysis] = useState(null);

//   useEffect(() => {
//     const fetchWeakConcepts = async () => {
//       try {
//         const res = await fetch(
//           `http://127.0.0.1:8000/api/agent/weak_concepts/${studentId}`
//         );

//         const data = await res.json();

//         // Try parsing JSON if the backend returned a JSON string
//         let parsed = null;
//         try {
//           parsed = JSON.parse(data.agent_analysis);
//         } catch {
//           parsed = data.agent_analysis;
//         }

//         setAnalysis(parsed);
//       } catch (err) {
//         console.error("Weak concept fetch error:", err);
//       }
//       setLoading(false);
//     };

//     fetchWeakConcepts();
//   }, []);

//   if (loading) {
//     return (
//       <div className="min-h-screen flex items-center justify-center text-white text-2xl">
//         ⏳ Loading...
//       </div>
//     );
//   }

//   return (
//     <div className="min-h-screen bg-gradient-to-br from-purple-500 to-indigo-600 p-10 text-white">
//       <h1 className="text-4xl font-bold mb-6">🔍 Weak Concepts</h1>

//       {/* Concepts List */}
//       <div className="space-y-4">
//         {analysis?.weak_concepts?.map((item, i) => (
//           <div
//             key={i}
//             className="bg-white/20 backdrop-blur-md rounded-xl p-5 border border-white/30 shadow-lg"
//           >
//             <h3 className="text-xl font-semibold text-yellow-300 mb-2">
//               {i + 1}. {item.concept}
//             </h3>
//             <p className="text-gray-200">{item.why_weak}</p>
//           </div>
//         ))}
//       </div>

//       {/* Summary */}
//       <div className="mt-8 bg-white/10 p-5 rounded-xl border border-white/20 backdrop-blur-md">
//         <h2 className="text-2xl font-semibold mb-2 text-green-300">📌 Summary</h2>
//         <p className="text-gray-200">{analysis?.summary}</p>
//       </div>

//       {/* ===== Agent Navigation Buttons ===== */}
//       <div className="text-center mt-10 space-y-3 w-full max-w-xl mx-auto">
//         <button
//           onClick={() => navigate("/agent/learning-path")}
//           className="w-full bg-white/30 text-white px-6 py-3 rounded-xl font-semibold hover:bg-white/40 transition"
//         >
//           📚 Personalized Learning Path
//         </button>

//         <button
//           onClick={() => navigate("/agent/exam-readiness")}
//           className="w-full bg-white/30 text-white px-6 py-3 rounded-xl font-semibold hover:bg-white/40 transition"
//         >
//           🎯 Exam Readiness Report
//         </button>

//         <button
//           onClick={() => navigate("/agent/practice-questions")}
//           className="w-full bg-white/30 text-white px-6 py-3 rounded-xl font-semibold hover:bg-white/40 transition"
//         >
//           ✏ Practice Questions (AI Generated)
//         </button>

//         <button
//           onClick={() => navigate("/evaluation")}
//           className="w-full bg-white text-purple-700 px-6 py-3 rounded-xl font-semibold hover:bg-gray-200 transition"
//         >
//           🔙 Back to Evaluation
//         </button>
//       </div>
//     </div>
//   );
// };

// export default WeakConcepts;


// import React, { useEffect, useState } from "react";
// import { useNavigate } from "react-router-dom";

// const WeakConcepts = () => {
//   const navigate = useNavigate();
//   const studentId = "student_123";

//   const [loading, setLoading] = useState(true);
//   const [analysis, setAnalysis] = useState(null);
//   const [error, setError] = useState(null);

//   useEffect(() => {
//     const fetchWeakConcepts = async () => {
//       try {
//         const res = await fetch(
//           `http://127.0.0.1:8000/api/agent/weak_concepts/${studentId}`
//         );

//         const data = await res.json();
//         console.log("🔥 RAW WEAK CONCEPTS:", data);

//         if (!data.agent_analysis) {
//           setError("No weak concepts found.");
//           setLoading(false);
//           return;
//         }

//         // Try parsing JSON string
//         let parsed;
//         try {
//           parsed = JSON.parse(data.agent_analysis);
//         } catch {
//           parsed = data.agent_analysis;
//         }

//         setAnalysis(parsed);
//       } catch (err) {
//         console.error(err);
//         setError("Network or server error.");
//       }

//       setLoading(false);
//     };

//     fetchWeakConcepts();
//   }, []);

//   // Loading Screen
//   if (loading) {
//     return (
//       <div className="min-h-screen flex items-center justify-center text-white text-3xl">
//         ⏳ Loading Weak Concepts...
//       </div>
//     );
//   }

//   // Error Screen
//   if (error) {
//     return (
//       <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-purple-600 to-pink-600 text-white text-3xl">
//         ⚠️ {error}
//         <button
//           onClick={() => navigate("/evaluation")}
//           className="mt-6 bg-white text-indigo-700 px-6 py-3 rounded-xl font-semibold hover:bg-gray-100 transition"
//         >
//           Go Back
//         </button>
//       </div>
//     );
//   }

//   // MAIN UI
//   return (
//     <div className="min-h-screen bg-gradient-to-br from-purple-600 to-indigo-600 p-10 text-white">
//       <h1 className="text-4xl font-extrabold mb-10">🔍 Weak Concepts</h1>

//       {/* Weak Concepts */}
//       <div className="space-y-6">
//         {analysis?.weak_concepts?.map((item, i) => (
//           <div
//             key={i}
//             className="bg-white/20 backdrop-blur-md p-6 rounded-2xl border border-white/30 shadow-xl"
//           >
//             <h2 className="text-xl font-semibold text-yellow-300 mb-2">
//               {i + 1}. {item.concept}
//             </h2>

//             <p className="text-gray-200">{item.why_weak}</p>
//           </div>
//         ))}
//       </div>

//       {/* Summary */}
//       <div className="bg-white/10 p-6 rounded-xl border border-white/20 mt-8">
//         <h2 className="text-2xl font-semibold text-green-300 mb-2">📘 Summary</h2>
//         <p className="text-gray-200">{analysis?.summary}</p>
//       </div>

//       <div className="text-center mt-10">
//         <button
//           onClick={() => navigate("/evaluation")}
//           className="bg-white text-blue-700 px-6 py-3 rounded-xl font-semibold hover:bg-gray-100 transition"
//         >
//           📑 Other Agents
//         </button>
//       </div>
//     </div>
//   );
// };

// export default WeakConcepts;


import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

const WeakConcepts = () => {
  const navigate = useNavigate();
  const studentId = "student_123";

  const [loading, setLoading] = useState(true);
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch(`http://127.0.0.1:8000/api/agent/weak_concepts/${studentId}`)
      .then((res) => res.json())
      .then((res) => {
        if (!res.weak_concepts || res.weak_concepts.length === 0) {
          setError("No weak concepts found.");
        } else {
          setData(res);
        }
        setLoading(false);
      })
      .catch(() => {
        setError("Server error");
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center text-white text-3xl">
        ⏳ Loading Weak Concepts...
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-purple-600 to-pink-600 text-white">
        ⚠️ {error}
        <button
          onClick={() => navigate("/evaluation")}
          className="mt-6 bg-white text-indigo-700 px-6 py-3 rounded-xl font-semibold"
        >
          Go Back
        </button>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-600 to-indigo-600 p-10 text-white">
      <h1 className="text-4xl font-extrabold mb-10">🔍 Weak Concepts (Explainable AI)</h1>

      {/* Weak Concepts */}
      <div className="space-y-6">
        {data.weak_concepts.map((item, i) => (
          <div
            key={i}
            className="bg-white/20 backdrop-blur-md p-6 rounded-2xl border border-white/30 shadow-xl"
          >
            <h2 className="text-xl font-semibold text-yellow-300 mb-2">
              {i + 1}. {item.concept}
            </h2>

            <p className="text-gray-200 mb-4">{item.why_weak}</p>

            {/* Explainability */}
            <div className="bg-white/10 p-4 rounded-xl">
              <h3 className="text-lg font-semibold mb-2">
                🔍 Explainability (SHAP/LIME)
              </h3>

              {(data.numeric_explainability.details[item.concept] || []).map(
                (exp, idx) => (
                  <p key={idx} className="text-sm text-gray-100">
                    • <b>{exp.feature}</b>: {exp.impact} (
                    <span
                      className={
                        exp.direction === "negative"
                          ? "text-red-300"
                          : "text-green-300"
                      }
                    >
                      {exp.direction}
                    </span>
                    )
                  </p>
                )
              )}
            </div>
          </div>
        ))}
      </div>

      {/* Summary */}
      <div className="bg-white/10 p-6 rounded-xl border border-white/20 mt-10">
        <h2 className="text-2xl font-semibold text-green-300 mb-2">📘 Summary</h2>
        <p className="text-gray-200">{data.summary}</p>
      </div>

      <div className="text-center mt-10">
        <button
          onClick={() => navigate("/evaluation")}
          className="bg-white text-blue-700 px-6 py-3 rounded-xl font-semibold"
        >
          📑 Other Agents
        </button>
      </div>
    </div>
  );
};

export default WeakConcepts;
