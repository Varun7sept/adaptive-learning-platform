// import React, { useEffect, useState } from "react";

// const ExamReadiness = () => {
//   const [data, setData] = useState(null);

//   useEffect(() => {
//     fetch("http://127.0.0.1:8000/api/agent/exam_readiness/student_123")
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
//         <h1 className="text-3xl font-bold mb-4">🎯 Exam Readiness</h1>

//         <pre className="bg-black/30 p-4 rounded-xl overflow-auto">
//           {JSON.stringify(data, null, 2)}
//         </pre>
//       </div>
//     </div>
//   );
// };

// export default ExamReadiness;


// import React, { useEffect, useState } from "react";
// import { useNavigate } from "react-router-dom";

// const ExamReadiness = () => {
//   const navigate = useNavigate();
//   const [readiness, setReadiness] = useState(null);
//   const [loading, setLoading] = useState(true);

//   useEffect(() => {
//     fetch("http://127.0.0.1:8000/api/agent/exam_readiness/student_123")
//       .then((res) => res.json())
//       .then((res) => {
//         console.log("RAW EXAM READINESS:", res);

//         let output = res.exam_readiness || res.analysis || res || null;

//         if (!output) {
//           setReadiness(null);
//           setLoading(false);
//           return;
//         }

//         // If backend returns JSON string → parse it
//         if (typeof output === "string") {
//           try {
//             output = JSON.parse(output);
//           } catch (e) {
//             console.error("JSON PARSE ERROR:", e);
//             setReadiness(null);
//             setLoading(false);
//             return;
//           }
//         }

//         setReadiness(output);
//         setLoading(false);
//       })
//       .catch((err) => {
//         console.error(err);
//         setReadiness(null);
//         setLoading(false);
//       });
//   }, []);

//   if (loading) {
//     return (
//       <div className="min-h-screen flex items-center justify-center text-white text-2xl">
//         ⏳ Loading Exam Readiness...
//       </div>
//     );
//   }

//   if (!readiness) {
//     return (
//       <div className="min-h-screen flex flex-col items-center justify-center text-white text-3xl bg-gradient-to-br from-purple-600 to-pink-600">
//         ⚠️ No Results Found
//         <button
//           onClick={() => navigate("/evaluation")}
//           className="mt-6 bg-white text-indigo-700 px-6 py-3 rounded-xl font-semibold hover:bg-gray-100 transition"
//         >
//           Go Back
//         </button>
//       </div>
//     );
//   }

//   return (
//     <div className="min-h-screen bg-gradient-to-br from-purple-600 to-indigo-600 p-10 text-white">
//       <h1 className="text-4xl font-extrabold mb-10">🎯 Exam Readiness</h1>

//       {/* SCORE */}
//       <div className="bg-white/20 p-6 rounded-2xl border border-white/30 mb-6 shadow-xl">
//         <h2 className="text-2xl font-semibold text-yellow-300 mb-2">📊 Readiness Score</h2>
//         <p className="text-3xl text-white font-bold">{readiness.readiness_score} / 100</p>
//       </div>

//       {/* STRENGTHS */}
//       <div className="bg-white/20 p-6 rounded-2xl border border-white/30 mb-6">
//         <h2 className="text-2xl font-semibold text-green-300 mb-2">💪 Strengths</h2>
//         <ul className="list-disc ml-6 text-gray-100">
//           {readiness.strengths?.map((s, i) => <li key={i}>{s}</li>)}
//         </ul>
//       </div>

//       {/* WEAKNESSES */}
//       <div className="bg-white/20 p-6 rounded-2xl border border-white/30 mb-6">
//         <h2 className="text-2xl font-semibold text-red-300 mb-2">⚠ Weaknesses</h2>
//         <ul className="list-disc ml-6 text-gray-100">
//           {readiness.weaknesses?.map((w, i) => <li key={i}>{w}</li>)}
//         </ul>
//       </div>

//       {/* SUGGESTIONS */}
//       <div className="bg-white/20 p-6 rounded-2xl border border-white/30 mb-6">
//         <h2 className="text-2xl font-semibold text-blue-300 mb-2">📘 Suggestions</h2>
//         <ul className="list-disc ml-6 text-gray-100">
//           {readiness.suggestions?.map((s, i) => <li key={i}>{s}</li>)}
//         </ul>
//       </div>

//       <div className="text-center mt-10">
//         <button
//           onClick={() => navigate("/evaluation")}
//           className="bg-white text-blue-700 px-6 py-3 rounded-xl font-semibold hover:bg-gray-100 transition"
//         >
//           🔙 Other Agents
//         </button>
//       </div>
//     </div>
//   );
// };

// export default ExamReadiness;

import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

const ExamReadiness = () => {
  const navigate = useNavigate();
  const [readiness, setReadiness] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/agent/exam_readiness/student_123")
      .then((res) => res.json())
      .then((res) => {
        console.log("RAW EXAM READINESS:", res);

        let output = res.exam_readiness || res.analysis || res || null;

        if (!output) {
          setReadiness(null);
          setLoading(false);
          return;
        }

        if (typeof output === "string") {
          try {
            output = JSON.parse(output);
          } catch (e) {
            console.error("JSON PARSE ERROR:", e);
            setReadiness(null);
            setLoading(false);
            return;
          }
        }

        setReadiness(output);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setReadiness(null);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center text-white text-2xl">
        ⏳ Loading Exam Readiness...
      </div>
    );
  }

  if (!readiness) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center text-white text-3xl bg-gradient-to-br from-purple-600 to-pink-600">
        ⚠️ No Results Found
        <button
          onClick={() => navigate("/evaluation")}
          className="mt-6 bg-white text-indigo-700 px-6 py-3 rounded-xl font-semibold hover:bg-gray-100 transition"
        >
          Go Back
        </button>
      </div>
    );
  }

  // ✅ SAFE ACCESS TO SHAP & LIME
  const shapFeatures =
    readiness?.explainability?.shap?.features || [];

  const limeFeatures =
    readiness?.explainability?.lime?.features || [];

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-600 to-indigo-600 p-10 text-white">
      <h1 className="text-4xl font-extrabold mb-10">🎯 Exam Readiness</h1>

      {/* SCORE */}
      <div className="bg-white/20 p-6 rounded-2xl border border-white/30 mb-6 shadow-xl">
        <h2 className="text-2xl font-semibold text-yellow-300 mb-2">
          📊 Readiness Score
        </h2>
        <p className="text-3xl font-bold">
          {readiness.readiness_score} / 100
        </p>
      </div>

      {/* STRENGTHS */}
      <div className="bg-white/20 p-6 rounded-2xl border border-white/30 mb-6">
        <h2 className="text-2xl font-semibold text-green-300 mb-2">
          💪 Strengths
        </h2>
        <ul className="list-disc ml-6">
          {readiness.strengths?.map((s, i) => (
            <li key={i}>{s}</li>
          ))}
        </ul>
      </div>

      {/* WEAKNESSES */}
      <div className="bg-white/20 p-6 rounded-2xl border border-white/30 mb-6">
        <h2 className="text-2xl font-semibold text-red-300 mb-2">
          ⚠ Weaknesses
        </h2>
        <ul className="list-disc ml-6">
          {readiness.weaknesses?.map((w, i) => (
            <li key={i}>{w}</li>
          ))}
        </ul>
      </div>

      {/* SUGGESTIONS */}
      <div className="bg-white/20 p-6 rounded-2xl border border-white/30 mb-6">
        <h2 className="text-2xl font-semibold text-blue-300 mb-2">
          📘 Suggestions
        </h2>
        <ul className="list-disc ml-6">
          {readiness.suggestions?.map((s, i) => (
            <li key={i}>{s}</li>
          ))}
        </ul>
      </div>

      {/* ================= SHAP EXPLANATION ================= */}
      <div className="bg-white/20 p-6 rounded-2xl border border-white/30 mb-6">
        <h2 className="text-2xl font-semibold text-purple-300 mb-2">
          🔍 Why did I get this score? (SHAP)
        </h2>

        {shapFeatures.length === 0 ? (
          <p>No SHAP explanation available.</p>
        ) : (
          <ul className="list-disc ml-6">
            {shapFeatures.map((item, index) => (
              <li key={index}>
                <strong>{item.feature}</strong>{" "}
                {item.direction === "positive"
                  ? "increased"
                  : "decreased"}{" "}
                your score
              </li>
            ))}
          </ul>
        )}
      </div>

      {/* ================= LIME EXPLANATION ================= */}
      <div className="bg-white/20 p-6 rounded-2xl border border-white/30 mb-6">
        <h2 className="text-2xl font-semibold text-pink-300 mb-2">
          🔎 What affects my score right now? (LIME)
        </h2>

        {limeFeatures.length === 0 ? (
          <p>No LIME explanation available.</p>
        ) : (
          <ul className="list-disc ml-6">
            {limeFeatures.map((item, index) => (
              <li key={index}>
                <strong>{item.feature}</strong>{" "}
                {item.direction === "positive"
                  ? "helps improve readiness"
                  : "reduces readiness"}
              </li>
            ))}
          </ul>
        )}
      </div>

      <div className="text-center mt-10">
        <button
          onClick={() => navigate("/evaluation")}
          className="bg-white text-blue-700 px-6 py-3 rounded-xl font-semibold hover:bg-gray-100 transition"
        >
          🔙 Other Agents
        </button>
      </div>
    </div>
  );
};

export default ExamReadiness;
