// import React from "react";
// import { useLocation, useNavigate } from "react-router-dom";
// import { CheckCircle2, XCircle } from "lucide-react";

// const QuizEvaluation = () => {
//   const location = useLocation();
//   const navigate = useNavigate();

//   // Get result & quizData from UploadMaterial.jsx
//   const { result, quizData } = location.state || {};

//   if (!result || !quizData) {
//     return (
//       <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 text-white">
//         <h2 className="text-3xl font-bold mb-4">⚠️ No Results Found</h2>
//         <button
//           onClick={() => navigate("/")}
//           className="bg-white text-indigo-700 font-semibold px-6 py-3 rounded-xl hover:bg-indigo-100 transition-all"
//         >
//           Go Back
//         </button>
//       </div>
//     );
//   }

//   // Extract details from result
//   const detailedResults = result?.detailed_results || [];
//   const [correctCount, total] = result?.score?.split("/") || [
//     0,
//     quizData.length,
//   ];

//   return (
//     <div className="min-h-screen bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 flex flex-col items-center justify-center text-white p-6">
//       <div className="bg-white/20 backdrop-blur-md rounded-3xl shadow-2xl p-10 w-full max-w-3xl border border-white/30">
//         <h1 className="text-4xl font-extrabold text-center mb-6">
//           🧾 Quiz Evaluation
//         </h1>

//         <div className="text-center mb-8">
//           <h2 className="text-2xl font-semibold mb-2">Your Score</h2>
//           <p className="text-5xl font-bold text-green-300">
//             {correctCount} / {total}
//           </p>
//         </div>

//         <div className="space-y-6">
//           {detailedResults.map((res, i) => (
//             <div
//               key={i}
//               className={`p-5 rounded-2xl ${
//                 res.is_correct ? "bg-green-400/20" : "bg-red-400/20"
//               } border border-white/30`}
//             >
//               <p className="font-semibold mb-2">
//                 {i + 1}. {res.question}
//               </p>

//               <p className="text-sm text-gray-200 mb-1">
//                 Your Answer:{" "}
//                 <span className="font-medium text-white">
//                   {res.selected || "Not answered"}
//                 </span>
//               </p>

//               <p className="text-sm text-gray-200 mb-2">
//                 Correct Answer:{" "}
//                 <span className="font-medium text-white">
//                   {res.correct}
//                 </span>
//               </p>

//               <div className="mt-3">
//                 {res.is_correct ? (
//                   <>
//                     <CheckCircle2 className="text-green-300 inline mr-2" />
//                     <span className="text-green-300 font-medium">Correct</span>
//                   </>
//                 ) : (
//                   <>
//                     <XCircle className="text-red-300 inline mr-2" />
//                     <span className="text-red-300 font-medium">Incorrect</span>
//                   </>
//                 )}
//               </div>
//             </div>
//           ))}
//         </div>

//         <div className="text-center mt-10">
//           <button
//             onClick={() => navigate("/")}
//             className="bg-white text-indigo-600 font-semibold px-6 py-3 rounded-xl hover:bg-indigo-100 transition-all"
//           >
//             Back to Quiz Generator
//           </button>
          
//         </div>
//       </div>
//     </div>
//   );
// };

// export default QuizEvaluation;




// import React from "react";
// import { useLocation, useNavigate } from "react-router-dom";
// import { CheckCircle2, XCircle } from "lucide-react";

// const QuizEvaluation = () => {
//   const location = useLocation();
//   const navigate = useNavigate();

//   // Get result & quizData from UploadMaterial.jsx
//   const { result, quizData } = location.state || {};

//   if (!result || !quizData) {
//     return (
//       <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 text-white">
//         <h2 className="text-3xl font-bold mb-4">⚠️ No Results Found</h2>
//         <button
//           onClick={() => navigate("/")}
//           className="bg-white text-indigo-700 font-semibold px-6 py-3 rounded-xl hover:bg-indigo-100 transition-all"
//         >
//           Go Back
//         </button>
//       </div>
//     );
//   }

//   // Extract details from result
//   const detailedResults = result?.detailed_results || [];
//   const [correctCount, total] = result?.score?.split("/") || [
//     0,
//     quizData.length,
//   ];

//   return (
//     <div className="min-h-screen bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 flex flex-col items-center justify-center text-white p-6">
//       <div className="bg-white/20 backdrop-blur-md rounded-3xl shadow-2xl p-10 w-full max-w-3xl border border-white/30">
//         <h1 className="text-4xl font-extrabold text-center mb-6">
//           🧾 Quiz Evaluation
//         </h1>

//         <div className="text-center mb-8">
//           <h2 className="text-2xl font-semibold mb-2">Your Score</h2>
//           <p className="text-5xl font-bold text-green-300">
//             {correctCount} / {total}
//           </p>
//         </div>

//         <div className="space-y-6">
//           {detailedResults.map((res, i) => (
//             <div
//               key={i}
//               className={`p-5 rounded-2xl ${
//                 res.is_correct ? "bg-green-400/20" : "bg-red-400/20"
//               } border border-white/30`}
//             >
//               <p className="font-semibold mb-2">
//                 {i + 1}. {res.question}
//               </p>

//               <p className="text-sm text-gray-200 mb-1">
//                 Your Answer:{" "}
//                 <span className="font-medium text-white">
//                   {res.selected || "Not answered"}
//                 </span>
//               </p>

//               <p className="text-sm text-gray-200 mb-2">
//                 Correct Answer:{" "}
//                 <span className="font-medium text-white">
//                   {res.correct}
//                 </span>
//               </p>

//               <div className="mt-3">
//                 {res.is_correct ? (
//                   <>
//                     <CheckCircle2 className="text-green-300 inline mr-2" />
//                     <span className="text-green-300 font-medium">Correct</span>
//                   </>
//                 ) : (
//                   <>
//                     <XCircle className="text-red-300 inline mr-2" />
//                     <span className="text-red-300 font-medium">Incorrect</span>
//                   </>
//                 )}
//               </div>
//             </div>
//           ))}
//         </div>

//         {/* ============ BACK BUTTON + AGENT BUTTONS ============ */}
//         <div className="text-center mt-10 space-y-3">
//           <button
//             onClick={() => navigate("/")}
//             className="bg-white text-indigo-600 font-semibold px-6 py-3 rounded-xl hover:bg-indigo-100 transition-all w-full"
//           >
//             Back to Quiz Generator
//           </button>

//           <button
//             onClick={() => navigate("/agent/weak")}
//             className="bg-white/30 text-white font-semibold px-6 py-3 rounded-xl hover:bg-white/40 transition-all w-full"
//           >
//             🔍 View Weak Concepts
//           </button>

//           <button
//             onClick={() => navigate("/agent/learning-path")}
//             className="bg-white/30 text-white font-semibold px-6 py-3 rounded-xl hover:bg-white/40 transition-all w-full"
//           >
//             📚 Personalized Learning Path
//           </button>

//           <button
//             onClick={() => navigate("/agent/exam-readiness")}
//             className="bg-white/30 text-white font-semibold px-6 py-3 rounded-xl hover:bg-white/40 transition-all w-full"
//           >
//             🎯 Exam Readiness Report
//           </button>

//           <button
//             onClick={() => navigate("/agent/practice-questions")}
//             className="bg-white/30 text-white font-semibold px-6 py-3 rounded-xl hover:bg-white/40 transition-all w-full"
//           >
//             ✏ Practice Questions (AI Generated)
//           </button>
//         </div>
//       </div>
//     </div>
//   );
// };

// export default QuizEvaluation;



import React, { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { CheckCircle2, XCircle } from "lucide-react";

const QuizEvaluation = () => {
  const location = useLocation();
  const navigate = useNavigate();

  const [result, setResult] = useState(null);
  const [quizData, setQuizData] = useState(null);

  // -------------------------------
  // Load data from location.state OR localStorage
  // -------------------------------
  useEffect(() => {
    const locResult = location.state?.result;
    const locQuiz = location.state?.quizData;

    if (locResult && locQuiz) {
      // Save to localStorage once
      localStorage.setItem("eval_result", JSON.stringify(locResult));
      localStorage.setItem("eval_quizData", JSON.stringify(locQuiz));

      setResult(locResult);
      setQuizData(locQuiz);
    } else {
      // Load from localStorage (when coming back from other agents)
      const storedResult = localStorage.getItem("eval_result");
      const storedQuiz = localStorage.getItem("eval_quizData");

      if (storedResult && storedQuiz) {
        setResult(JSON.parse(storedResult));
        setQuizData(JSON.parse(storedQuiz));
      }
    }
  }, [location.state]);

  // -------------------------------
  // STILL LOADING
  // -------------------------------
  if (!result || !quizData) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 text-white">
        <h2 className="text-3xl font-bold mb-4">⏳ Loading Evaluation...</h2>
      </div>
    );
  }

  // Extract details
  const detailedResults = result?.detailed_results || [];
  const [correctCount, total] = result?.score?.split("/") || [
    0,
    quizData.length,
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 flex flex-col items-center justify-center text-white p-6">
      <div className="bg-white/20 backdrop-blur-md rounded-3xl shadow-2xl p-10 w-full max-w-3xl border border-white/30">

        <h1 className="text-4xl font-extrabold text-center mb-6">
          🧾 Quiz Evaluation
        </h1>

        {/* Score */}
        <div className="text-center mb-8">
          <h2 className="text-2xl font-semibold mb-2">Your Score</h2>
          <p className="text-5xl font-bold text-green-300">
            {correctCount} / {total}
          </p>
        </div>

        {/* Questions Review */}
        <div className="space-y-6">
          {detailedResults.map((res, i) => (
            <div
              key={i}
              className={`p-5 rounded-2xl ${
                res.is_correct ? "bg-green-400/20" : "bg-red-400/20"
              } border border-white/30`}
            >
              <p className="font-semibold mb-2">
                {i + 1}. {res.question}
              </p>

              <p className="text-sm text-gray-200 mb-1">
                Your Answer:{" "}
                <span className="font-medium text-white">
                  {res.selected || "Not answered"}
                </span>
              </p>

              <p className="text-sm text-gray-200 mb-2">
                Correct Answer:{" "}
                <span className="font-medium text-white">{res.correct}</span>
              </p>

              <div className="mt-3">
                {res.is_correct ? (
                  <>
                    <CheckCircle2 className="text-green-300 inline mr-2" />
                    <span className="text-green-300 font-medium">Correct</span>
                  </>
                ) : (
                  <>
                    <XCircle className="text-red-300 inline mr-2" />
                    <span className="text-red-300 font-medium">Incorrect</span>
                  </>
                )}
              </div>
            </div>
          ))}
        </div>

        {/* Buttons */}
        <div className="text-center mt-10 space-y-3">
          <button
            onClick={() => navigate("/")}
            className="bg-white text-indigo-600 font-semibold px-6 py-3 rounded-xl hover:bg-indigo-100 transition-all w-full"
          >
            Back to Quiz Generator
          </button>

          <button
            onClick={() => navigate("/agent/weak")}
            className="bg-white/30 text-white font-semibold px-6 py-3 rounded-xl hover:bg-white/40 transition-all w-full"
          >
            🔍 View Weak Concepts
          </button>

          <button
            onClick={() => navigate("/agent/learning-path")}
            className="bg-white/30 text-white font-semibold px-6 py-3 rounded-xl hover:bg-white/40 transition-all w-full"
          >
            📚 Personalized Learning Path
          </button>

          <button
            onClick={() => navigate("/agent/exam-readiness")}
            className="bg-white/30 text-white font-semibold px-6 py-3 rounded-xl hover:bg-white/40 transition-all w-full"
          >
            🎯 Exam Readiness Report
          </button>

          <button
            onClick={() => navigate("/agent/practice-questions")}
            className="bg-white/30 text-white font-semibold px-6 py-3 rounded-xl hover:bg-white/40 transition-all w-full"
          >
            ✏ Practice Questions (AI Generated)
          </button>
        </div>
      </div>
    </div>
  );
};

export default QuizEvaluation;
