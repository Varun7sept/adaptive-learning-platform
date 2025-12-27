// import React, { useState } from "react";
// import { useNavigate } from "react-router-dom";
// import { CloudUpload, Loader2 } from "lucide-react";

// const UploadMaterial = () => {
//   const [file, setFile] = useState(null);
//   const [numQuestions, setNumQuestions] = useState(5);
//   const [loading, setLoading] = useState(false);
//   const [message, setMessage] = useState("");
//   const [quizData, setQuizData] = useState(null);
//   const [answers, setAnswers] = useState({});
//   const navigate = useNavigate();

//   const handleFileChange = (e) => setFile(e.target.files[0]);

//   // 📘 Parse AI text output into structured quiz format
//   const parseQuiz = (rawText) => {
//     const lines = rawText.split("\n").filter((line) => line.trim() !== "");
//     const questions = [];
//     let current = { question: "", options: [], correct: "" };

//     lines.forEach((line) => {
//       if (/^\d+\./.test(line)) {
//         if (current.question) questions.push(current);
//         current = { question: line, options: [], correct: "" };
//       } else if (/^[a-d]\)/.test(line.trim())) {
//         current.options.push(line.trim());
//       } else if (line.toLowerCase().includes("correct answer")) {
//         current.correct = line.split(":")[1]?.trim();
//       }
//     });

//     if (current.question) questions.push(current);
//     return questions;
//   };

//   // 📤 Upload and generate quiz
//   const handleSubmit = async (e) => {
//     e.preventDefault();
//     if (!file) return setMessage("⚠️ Please upload a file first!");
//     setLoading(true);
//     setMessage("");
//     setQuizData(null);

//     try {
//       const formData = new FormData();
//       formData.append("file", file);
//       formData.append("num_questions", numQuestions);

//       const response = await fetch("http://127.0.0.1:8000/api/quiz/upload", {
//         method: "POST",
//         body: formData,
//       });

//       if (!response.ok) throw new Error("Quiz generation failed");
//       const data = await response.json();

//       const parsed = parseQuiz(data.generated_quiz.quiz_questions);
//       setQuizData(parsed);
//       setMessage("✅ Quiz generated successfully!");
//     } catch (error) {
//       console.error(error);
//       setMessage("❌ Failed to generate quiz. Please try again.");
//     } finally {
//       setLoading(false);
//     }
//   };

//   // 📩 Track selected answers
//   const handleAnswerChange = (qIndex, answer) => {
//     setAnswers((prev) => ({ ...prev, [qIndex]: answer }));
//   };

//   // 📬 Submit answers for evaluation (frontend-managed)
//   const handleEvaluate = async () => {
//     try {
//       // Build evaluation object that matches your backend expectation
//       const userAnswers = quizData.map((q, i) => ({
//         question: q.question,
//         selected: answers[i] || "Not answered",
//         correct: q.correct,
//         is_correct:
//           (answers[i] || "").trim().toLowerCase() ===
//           (q.correct || "").trim().toLowerCase(),
//       }));

//       // Compute score locally since backend doesn't handle it fully
//       const correctCount = userAnswers.filter((a) => a.is_correct).length;
//       const score = `${correctCount} / ${quizData.length}`;

//       const result = {
//         score,
//         detailed_results: userAnswers,
//       };

//       // ✅ Navigate to evaluation page with results
//       navigate("/evaluation", { state: { result, quizData } });
//     } catch (err) {
//       console.error("Evaluation failed:", err);
//       setMessage("❌ Evaluation failed. Please try again.");
//     }
//   };

//   return (
//     <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 text-white p-4">
//       <div className="bg-white/20 backdrop-blur-md shadow-2xl rounded-3xl p-10 w-full max-w-2xl border border-white/30 transition-all">
//         <h1 className="text-3xl font-extrabold text-center mb-6">
//           🧠 Adaptive Learning Platform
//         </h1>

//         {/* Upload Form */}
//         <form onSubmit={handleSubmit} className="space-y-6">
//           {/* File Upload */}
//           <div className="border-2 border-dashed border-white/60 rounded-2xl p-6 text-center cursor-pointer hover:bg-white/10 transition">
//             <CloudUpload className="w-10 h-10 text-white mx-auto mb-3" />
//             <label htmlFor="file" className="cursor-pointer font-medium">
//               {file ? file.name : "Choose a file to upload"}
//             </label>
//             <input
//               id="file"
//               type="file"
//               onChange={handleFileChange}
//               className="hidden"
//               accept=".pdf,.txt,.docx"
//             />
//           </div>

//           {/* Number of Questions */}
//           <div>
//             <label className="block text-sm font-semibold mb-2">
//               Number of Questions
//             </label>
//             <input
//               type="number"
//               value={numQuestions}
//               onChange={(e) => setNumQuestions(e.target.value)}
//               min="1"
//               max="20"
//               className="w-full p-3 rounded-xl bg-white/20 border border-white/30 text-white placeholder-gray-200 focus:outline-none focus:ring-2 focus:ring-pink-400"
//             />
//           </div>

//           {/* Generate Quiz Button */}
//           <button
//             type="submit"
//             disabled={loading}
//             className="w-full flex items-center justify-center gap-2 bg-gradient-to-r from-pink-500 to-indigo-500 text-white font-semibold py-3 px-4 rounded-xl hover:opacity-90 transition-all duration-300 disabled:opacity-70"
//           >
//             {loading ? (
//               <>
//                 <Loader2 className="w-5 h-5 animate-spin" /> Generating Quiz...
//               </>
//             ) : (
//               <>
//                 <CloudUpload className="w-5 h-5" /> Generate Quiz
//               </>
//             )}
//           </button>
//         </form>

//         {/* Message Display */}
//         {message && (
//           <p
//             className={`mt-4 text-center font-medium ${
//               message.startsWith("✅") ? "text-green-300" : "text-red-300"
//             }`}
//           >
//             {message}
//           </p>
//         )}

//         {/* Quiz Section */}
//         {quizData && (
//           <div className="mt-8 bg-white/10 p-6 rounded-2xl border border-white/20">
//             <h2 className="text-2xl font-bold mb-4">📝 Generated Quiz</h2>
//             {quizData.map((q, i) => (
//               <div key={i} className="mb-6">
//                 <p className="font-semibold mb-2">{q.question}</p>
//                 {q.options.map((opt, j) => (
//                   <label
//                     key={j}
//                     className="block mb-1 cursor-pointer hover:text-pink-200"
//                   >
//                     <input
//                       type="radio"
//                       name={`question-${i}`}
//                       value={opt}
//                       onChange={() => handleAnswerChange(i, opt)}
//                       className="mr-2 accent-pink-400"
//                     />
//                     {opt}
//                   </label>
//                 ))}
//               </div>
//             ))}

//             <button
//               onClick={handleEvaluate}
//               className="mt-4 w-full bg-green-500 hover:bg-green-600 text-white font-semibold py-3 rounded-xl transition-all"
//             >
//               Submit Answers
//             </button>
//           </div>
//         )}
//       </div>

//       <p className="text-white mt-6 text-sm opacity-80">
//         © {new Date().getFullYear()} Adaptive Learning Platform
//       </p>
//     </div>
//   );
// };

// export default UploadMaterial;


// import React, { useState } from "react";
// import { useNavigate } from "react-router-dom";
// import { CloudUpload, Loader2 } from "lucide-react";

// const UploadMaterial = () => {
//   const [file, setFile] = useState(null);
//   const [numQuestions, setNumQuestions] = useState(5);
//   const [loading, setLoading] = useState(false);
//   const [message, setMessage] = useState("");
//   const [quizData, setQuizData] = useState(null);
//   const [answers, setAnswers] = useState({});
//   const navigate = useNavigate();

//   const handleFileChange = (e) => setFile(e.target.files[0]);

//   // 📘 Parse AI text output into structured quiz format
//   const parseQuiz = (rawText) => {
//     const lines = rawText.split("\n").filter((line) => line.trim() !== "");
//     const questions = [];
//     let current = { question: "", options: [], correct: "" };

//     lines.forEach((line) => {
//       if (/^\d+\./.test(line)) {
//         if (current.question) questions.push(current);
//         current = { question: line, options: [], correct: "" };
//       } else if (/^[a-d]\)/.test(line.trim())) {
//         current.options.push(line.trim());
//       } else if (line.toLowerCase().includes("correct answer")) {
//         current.correct = line.split(":")[1]?.trim();
//       }
//     });

//     if (current.question) questions.push(current);
//     return questions;
//   };

//   // 📤 Upload and generate quiz
//   const handleSubmit = async (e) => {
//     e.preventDefault();
//     if (!file) return setMessage("⚠️ Please upload a file first!");
//     setLoading(true);
//     setMessage("");
//     setQuizData(null);

//     try {
//       const formData = new FormData();
//       formData.append("file", file);
//       formData.append("num_questions", numQuestions);

//       const response = await fetch("http://127.0.0.1:8000/api/quiz/upload", {
//         method: "POST",
//         body: formData,
//       });

//       if (!response.ok) throw new Error("Quiz generation failed");
//       const data = await response.json();

//       const parsed = parseQuiz(data.generated_quiz.quiz_questions);
//       setQuizData(parsed);
//       setMessage("✅ Quiz generated successfully!");
//     } catch (error) {
//       console.error(error);
//       setMessage("❌ Failed to generate quiz. Please try again.");
//     } finally {
//       setLoading(false);
//     }
//   };

//   // 📩 Track selected answers
//   const handleAnswerChange = (qIndex, answer) => {
//     setAnswers((prev) => ({ ...prev, [qIndex]: answer }));
//   };

//   // 📬 Submit answers for evaluation (calls backend AND preserves frontend detailed_results)
//   const handleEvaluate = async () => {
//     try {
//       if (!quizData) {
//         setMessage("⚠️ No quiz available to evaluate.");
//         return;
//       }

//       // Build detailed results exactly like before (so QuizEvaluation.jsx works)
//       const userAnswers = quizData.map((q, i) => {
//         const selected = answers[i] || "Not answered";
//         const is_correct =
//           (selected || "").trim().toLowerCase() ===
//           (q.correct || "").trim().toLowerCase();

//         return {
//           question: q.question,
//           selected,
//           correct: q.correct,
//           is_correct,
//         };
//       });

//       const correctCount = userAnswers.filter((a) => a.is_correct).length;
//       const scoreString = `${correctCount} / ${quizData.length}`;

//       // Prepare payload to backend (send the textual questions + student answers)
//       const studentAnswersText = userAnswers
//         .map((ua, idx) => `${idx + 1}. ${ua.selected}`)
//         .join("\n");

//       const questionsText = quizData
//         .map(
//           (q, idx) =>
//             `${idx + 1}. ${q.question}\n${q.options.join("\n")}\nCorrect: ${q.correct}`
//         )
//         .join("\n\n");

//       const payload = {
//         questions: questionsText,
//         student_answers: studentAnswersText,
//         student_id: "student_123",
//         quiz_id: "quiz_" + Date.now(),
//       };

//       // Fire-and-forget backend call (we'll still navigate even if it fails)
//       try {
//         const res = await fetch("http://127.0.0.1:8000/api/quiz/evaluate", {
//           method: "POST",
//           headers: { "Content-Type": "application/json" },
//           body: JSON.stringify(payload),
//         });

//         // optional: you can inspect backend response for debugging
//         if (!res.ok) {
//           console.warn("Backend evaluation returned non-OK status", res.status);
//         } else {
//           const data = await res.json();
//           // optional: show parsed score from backend if you want
//           console.log("Backend evaluation response:", data);
//         }
//       } catch (backendErr) {
//         // Don't block navigation — just log it
//         console.error("Error calling backend evaluate API:", backendErr);
//         setMessage("⚠️ Backend evaluate API failed (check logs).");
//       }

//       // Navigate to evaluation page with the same result structure your QuizEvaluation expects
//       const result = {
//         score: scoreString,
//         detailed_results: userAnswers,
//       };

//       navigate("/evaluation", { state: { result, quizData } });
//     } catch (err) {
//       console.error("Evaluation failed:", err);
//       setMessage("❌ Evaluation failed. Please try again.");
//     }
//   };

//   return (
//     <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 text-white p-4">
//       <div className="bg-white/20 backdrop-blur-md shadow-2xl rounded-3xl p-10 w-full max-w-2xl border border-white/30 transition-all">
//         <h1 className="text-3xl font-extrabold text-center mb-6">
//           🧠 Adaptive Learning Platform
//         </h1>

//         {/* Upload Form */}
//         <form onSubmit={handleSubmit} className="space-y-6">
//           {/* File Upload */}
//           <div className="border-2 border-dashed border-white/60 rounded-2xl p-6 text-center cursor-pointer hover:bg-white/10 transition">
//             <CloudUpload className="w-10 h-10 text-white mx-auto mb-3" />
//             <label htmlFor="file" className="cursor-pointer font-medium">
//               {file ? file.name : "Choose a file to upload"}
//             </label>
//             <input
//               id="file"
//               type="file"
//               onChange={handleFileChange}
//               className="hidden"
//               accept=".pdf,.txt,.docx"
//             />
//           </div>

//           {/* Number of Questions */}
//           <div>
//             <label className="block text-sm font-semibold mb-2">
//               Number of Questions
//             </label>
//             <input
//               type="number"
//               value={numQuestions}
//               onChange={(e) => setNumQuestions(e.target.value)}
//               min="1"
//               max="20"
//               className="w-full p-3 rounded-xl bg-white/20 border border-white/30 text-white placeholder-gray-200 focus:outline-none focus:ring-2 focus:ring-pink-400"
//             />
//           </div>

//           {/* Generate Quiz Button */}
//           <button
//             type="submit"
//             disabled={loading}
//             className="w-full flex items-center justify-center gap-2 bg-gradient-to-r from-pink-500 to-indigo-500 text-white font-semibold py-3 px-4 rounded-xl hover:opacity-90 transition-all duration-300 disabled:opacity-70"
//           >
//             {loading ? (
//               <>
//                 <Loader2 className="w-5 h-5 animate-spin" /> Generating Quiz...
//               </>
//             ) : (
//               <>
//                 <CloudUpload className="w-5 h-5" /> Generate Quiz
//               </>
//             )}
//           </button>
//         </form>

//         {/* Message Display */}
//         {message && (
//           <p
//             className={`mt-4 text-center font-medium ${
//               message.startsWith("✅") ? "text-green-300" : "text-red-300"
//             }`}
//           >
//             {message}
//           </p>
//         )}

//         {/* Quiz Section */}
//         {quizData && (
//           <div className="mt-8 bg-white/10 p-6 rounded-2xl border border-white/20">
//             <h2 className="text-2xl font-bold mb-4">📝 Generated Quiz</h2>
//             {quizData.map((q, i) => (
//               <div key={i} className="mb-6">
//                 <p className="font-semibold mb-2">{q.question}</p>
//                 {q.options.map((opt, j) => (
//                   <label
//                     key={j}
//                     className="block mb-1 cursor-pointer hover:text-pink-200"
//                   >
//                     <input
//                       type="radio"
//                       name={`question-${i}`}
//                       value={opt}
//                       onChange={() => handleAnswerChange(i, opt)}
//                       className="mr-2 accent-pink-400"
//                     />
//                     {opt}
//                   </label>
//                 ))}
//               </div>
//             ))}

//             <button
//               onClick={handleEvaluate}
//               className="mt-4 w-full bg-green-500 hover:bg-green-600 text-white font-semibold py-3 rounded-xl transition-all"
//             >
//               Submit Answers
//             </button>
//           </div>
//         )}
//       </div>

//       <p className="text-white mt-6 text-sm opacity-80">
//         © {new Date().getFullYear()} Adaptive Learning Platform
//       </p>
//     </div>
//   );
// };

// export default UploadMaterial;




// import React, { useState } from "react";
// import { useNavigate } from "react-router-dom";
// import { CloudUpload, Loader2 } from "lucide-react";

// const UploadMaterial = () => {
//   const [file, setFile] = useState(null);
//   const [numQuestions, setNumQuestions] = useState(5);
//   const [loading, setLoading] = useState(false);
//   const [message, setMessage] = useState("");
//   const [quizData, setQuizData] = useState(null);
//   const [answers, setAnswers] = useState({});
//   const navigate = useNavigate();

//   const handleFileChange = (e) => setFile(e.target.files[0]);

//   // 📘 Parse AI text output into structured quiz format
//   const parseQuiz = (rawText) => {
//     const lines = rawText.split("\n").filter((line) => line.trim() !== "");
//     const questions = [];
//     let current = { question: "", options: [], correct: "" };

//     lines.forEach((line) => {
//       if (/^\d+\./.test(line)) {
//         if (current.question) questions.push(current);
//         current = { question: line, options: [], correct: "" };
//       } else if (/^[a-d]\)/.test(line.trim())) {
//         current.options.push(line.trim());
//       } else if (line.toLowerCase().includes("correct answer")) {
//         current.correct = line.split(":")[1]?.trim();
//       }
//     });

//     if (current.question) questions.push(current);
//     return questions;
//   };

//   // 📤 Upload and generate quiz
//   const handleSubmit = async (e) => {
//     e.preventDefault();
//     if (!file) return setMessage("⚠️ Please upload a file first!");
//     setLoading(true);
//     setMessage("");
//     setQuizData(null);

//     try {
//       const formData = new FormData();
//       formData.append("file", file);
//       formData.append("num_questions", numQuestions);

//       const response = await fetch("http://127.0.0.1:8000/api/quiz/upload", {
//         method: "POST",
//         body: formData,
//       });

//       if (!response.ok) throw new Error("Quiz generation failed");
//       const data = await response.json();

//       const parsed = parseQuiz(data.generated_quiz.quiz_questions);
//       setQuizData(parsed);
//       setMessage("✅ Quiz generated successfully!");
//     } catch (error) {
//       console.error(error);
//       setMessage("❌ Failed to generate quiz. Please try again.");
//     } finally {
//       setLoading(false);
//     }
//   };

//   // 📩 Track selected answers
//   const handleAnswerChange = (qIndex, answer) => {
//     setAnswers((prev) => ({ ...prev, [qIndex]: answer }));
//   };

//   // 📬 Submit answers for evaluation (now includes detailed_results!)
//   const handleEvaluate = async () => {
//     try {
//       if (!quizData) {
//         setMessage("⚠️ No quiz available to evaluate.");
//         return;
//       }

//       // Build detailed results (frontend evaluation)
//       const userAnswers = quizData.map((q, i) => {
//         const selected = answers[i] || "Not answered";
//         const is_correct =
//           (selected || "").trim().toLowerCase() ===
//           (q.correct || "").trim().toLowerCase();

//         return {
//           question: q.question,
//           options: q.options,
//           selected,
//           correct: q.correct,
//           is_correct,
//         };
//       });

//       const correctCount = userAnswers.filter((a) => a.is_correct).length;
//       const scoreString = `${correctCount} / ${quizData.length}`;

//       // Build textual answer format for LLM
//       const studentAnswersText = userAnswers
//         .map((ua, idx) => `${idx + 1}. ${ua.selected}`)
//         .join("\n");

//       const questionsText = quizData
//         .map(
//           (q, idx) =>
//             `${idx + 1}. ${q.question}\n${q.options.join("\n")}\nCorrect: ${q.correct}`
//         )
//         .join("\n\n");

//       // 🚀 FINAL PAYLOAD with detailed_results
//       const payload = {
//         questions: questionsText,
//         student_answers: studentAnswersText,
//         student_id: "student_123",
//         quiz_id: "quiz_" + Date.now(),
//         detailed_results: userAnswers, // ⭐ NOW INCLUDED
//       };

//       // Send to backend
//       try {
//         const res = await fetch("http://127.0.0.1:8000/api/quiz/evaluate", {
//           method: "POST",
//           headers: { "Content-Type": "application/json" },
//           body: JSON.stringify(payload),
//         });

//         if (!res.ok) {
//           console.warn("Backend evaluate returned non-OK status", res.status);
//         } else {
//           const data = await res.json();
//           console.log("Backend evaluation response:", data);
//         }
//       } catch (backendErr) {
//         console.error("Backend evaluate API error:", backendErr);
//         setMessage("⚠️ Backend evaluate API failed.");
//       }

//       // Navigate to results page
//       const result = {
//         score: scoreString,
//         detailed_results: userAnswers,
//       };

//       navigate("/evaluation", { state: { result, quizData } });
//     } catch (err) {
//       console.error("Evaluation failed:", err);
//       setMessage("❌ Evaluation failed. Please try again.");
//     }
//   };

//   return (
//     <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 text-white p-4">
//       <div className="bg-white/20 backdrop-blur-md shadow-2xl rounded-3xl p-10 w-full max-w-2xl border border-white/30 transition-all">
//         <h1 className="text-3xl font-extrabold text-center mb-6">
//           🧠 Adaptive Learning Platform
//         </h1>

//         {/* Upload Form */}
//         <form onSubmit={handleSubmit} className="space-y-6">
//           {/* File Upload */}
//           <div className="border-2 border-dashed border-white/60 rounded-2xl p-6 text-center cursor-pointer hover:bg-white/10 transition">
//             <CloudUpload className="w-10 h-10 text-white mx-auto mb-3" />
//             <label htmlFor="file" className="cursor-pointer font-medium">
//               {file ? file.name : "Choose a file to upload"}
//             </label>
//             <input
//               id="file"
//               type="file"
//               onChange={handleFileChange}
//               className="hidden"
//               accept=".pdf,.txt,.docx"
//             />
//           </div>

//           {/* Number of Questions */}
//           <div>
//             <label className="block text-sm font-semibold mb-2">
//               Number of Questions
//             </label>
//             <input
//               type="number"
//               value={numQuestions}
//               onChange={(e) => setNumQuestions(e.target.value)}
//               min="1"
//               max="20"
//               className="w-full p-3 rounded-xl bg-white/20 border border-white/30 text-white placeholder-gray-200 focus:outline-none focus:ring-2 focus:ring-pink-400"
//             />
//           </div>

//           {/* Generate Quiz Button */}
//           <button
//             type="submit"
//             disabled={loading}
//             className="w-full flex items-center justify-center gap-2 bg-gradient-to-r from-pink-500 to-indigo-500 text-white font-semibold py-3 px-4 rounded-xl hover:opacity-90 transition-all duration-300 disabled:opacity-70"
//           >
//             {loading ? (
//               <>
//                 <Loader2 className="w-5 h-5 animate-spin" /> Generating Quiz...
//               </>
//             ) : (
//               <>
//                 <CloudUpload className="w-5 h-5" /> Generate Quiz
//               </>
//             )}
//           </button>
//         </form>

//         {/* Message */}
//         {message && (
//           <p
//             className={`mt-4 text-center font-medium ${
//               message.startsWith("✅") ? "text-green-300" : "text-red-300"
//             }`}
//           >
//             {message}
//           </p>
//         )}

//         {/* Quiz Section */}
//         {quizData && (
//           <div className="mt-8 bg-white/10 p-6 rounded-2xl border border-white/20">
//             <h2 className="text-2xl font-bold mb-4">📝 Generated Quiz</h2>
//             {quizData.map((q, i) => (
//               <div key={i} className="mb-6">
//                 <p className="font-semibold mb-2">{q.question}</p>
//                 {q.options.map((opt, j) => (
//                   <label
//                     key={j}
//                     className="block mb-1 cursor-pointer hover:text-pink-200"
//                   >
//                     <input
//                       type="radio"
//                       name={`question-${i}`}
//                       value={opt}
//                       onChange={() => handleAnswerChange(i, opt)}
//                       className="mr-2 accent-pink-400"
//                     />
//                     {opt}
//                   </label>
//                 ))}
//               </div>
//             ))}

//             <button
//               onClick={handleEvaluate}
//               className="mt-4 w-full bg-green-500 hover:bg-green-600 text-white font-semibold py-3 rounded-xl transition-all"
//             >
//               Submit Answers
//             </button>
//           </div>
//         )}
//       </div>

//       <p className="text-white mt-6 text-sm opacity-80">
//         © {new Date().getFullYear()} Adaptive Learning Platform
//       </p>
//     </div>
//   );
// };

// export default UploadMaterial;




import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { CloudUpload, Loader2 } from "lucide-react";

const UploadMaterial = () => {
  const [file, setFile] = useState(null);
  const [numQuestions, setNumQuestions] = useState(5);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [quizData, setQuizData] = useState(null);
  const [answers, setAnswers] = useState({});
  const navigate = useNavigate();

  const handleFileChange = (e) => setFile(e.target.files[0]);

  // 📘 Parse AI text output into structured quiz format
  const parseQuiz = (rawText) => {
    const lines = rawText.split("\n").filter((line) => line.trim() !== "");
    const questions = [];
    let current = { question: "", options: [], correct: "" };

    lines.forEach((line) => {
      if (/^\d+\./.test(line)) {
        if (current.question) questions.push(current);
        current = { question: line, options: [], correct: "" };
      } else if (/^[a-d]\)/.test(line.trim())) {
        current.options.push(line.trim());
      } else if (line.toLowerCase().includes("correct answer")) {
        current.correct = line.split(":")[1]?.trim();
      }
    });

    if (current.question) questions.push(current);
    return questions;
  };

  // 📤 Upload and generate quiz
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return setMessage("⚠️ Please upload a file first!");
    setLoading(true);
    setMessage("");
    setQuizData(null);

    try {
      const formData = new FormData();
      formData.append("file", file);
      formData.append("num_questions", numQuestions);

      const response = await fetch("http://127.0.0.1:8000/api/quiz/upload", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) throw new Error("Quiz generation failed");
      const data = await response.json();

      const parsed = parseQuiz(data.generated_quiz.quiz_questions);
      setQuizData(parsed);
      setMessage("✅ Quiz generated successfully!");
    } catch (error) {
      console.error(error);
      setMessage("❌ Failed to generate quiz. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  // 📩 Track selected answers
  const handleAnswerChange = (qIndex, answer) => {
    setAnswers((prev) => ({ ...prev, [qIndex]: answer }));
  };

  // 📬 Submit answers for evaluation (now includes detailed_results!)
  const handleEvaluate = async () => {
    try {
      if (!quizData) {
        setMessage("⚠️ No quiz available to evaluate.");
        return;
      }

      // Build detailed results (frontend evaluation)
      const userAnswers = quizData.map((q, i) => {
        const selected = answers[i] || "Not answered";
        const is_correct =
          (selected || "").trim().toLowerCase() ===
          (q.correct || "").trim().toLowerCase();

        return {
          question: q.question,
          options: q.options,
          selected,
          correct: q.correct,
          is_correct,
        };
      });

      const correctCount = userAnswers.filter((a) => a.is_correct).length;
      const scoreString = `${correctCount} / ${quizData.length}`;

      // Build textual answer format for LLM
      const studentAnswersText = userAnswers
        .map((ua, idx) => `${idx + 1}. ${ua.selected}`)
        .join("\n");

      const questionsText = quizData
        .map(
          (q, idx) =>
            `${idx + 1}. ${q.question}\n${q.options.join("\n")}\nCorrect: ${q.correct}`
        )
        .join("\n\n");

      // 🚀 FINAL PAYLOAD with detailed_results
      const payload = {
        questions: questionsText,
        student_answers: studentAnswersText,
        student_id: "student_123",
        quiz_id: "quiz_" + Date.now(),
        detailed_results: userAnswers, // ⭐ NOW INCLUDED
      };

      // Send to backend
      try {
        const res = await fetch("http://127.0.0.1:8000/api/quiz/evaluate", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });

        if (!res.ok) {
          console.warn("Backend evaluate returned non-OK status", res.status);
        } else {
          const data = await res.json();
          console.log("Backend evaluation response:", data);
        }
      } catch (backendErr) {
        console.error("Backend evaluate API error:", backendErr);
        setMessage("⚠️ Backend evaluate API failed.");
      }

      // Navigate to results page
      const result = {
        score: scoreString,
        detailed_results: userAnswers,
      };

      navigate("/evaluation", { state: { result, quizData } });
    } catch (err) {
      console.error("Evaluation failed:", err);
      setMessage("❌ Evaluation failed. Please try again.");
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 text-white p-4">
      <div className="bg-white/20 backdrop-blur-md shadow-2xl rounded-3xl p-10 w-full max-w-2xl border border-white/30 transition-all">
        <h1 className="text-3xl font-extrabold text-center mb-6">
          🧠 Adaptive Learning Platform
        </h1>

        {/* Upload Form */}
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* File Upload */}
          <div className="border-2 border-dashed border-white/60 rounded-2xl p-6 text-center cursor-pointer hover:bg-white/10 transition">
            <CloudUpload className="w-10 h-10 text-white mx-auto mb-3" />
            <label htmlFor="file" className="cursor-pointer font-medium">
              {file ? file.name : "Choose a file to upload"}
            </label>
            <input
              id="file"
              type="file"
              onChange={handleFileChange}
              className="hidden"
              accept=".pdf,.txt,.docx"
            />
          </div>

          {/* Number of Questions */}
          <div>
            <label className="block text-sm font-semibold mb-2">
              Number of Questions
            </label>
            <input
              type="number"
              value={numQuestions}
              onChange={(e) => setNumQuestions(e.target.value)}
              min="1"
              max="20"
              className="w-full p-3 rounded-xl bg-white/20 border border-white/30 text-white placeholder-gray-200 focus:outline-none focus:ring-2 focus:ring-pink-400"
            />
          </div>

          {/* Generate Quiz Button */}
          <button
            type="submit"
            disabled={loading}
            className="w-full flex items-center justify-center gap-2 bg-gradient-to-r from-pink-500 to-indigo-500 text-white font-semibold py-3 px-4 rounded-xl hover:opacity-90 transition-all duration-300 disabled:opacity-70"
          >
            {loading ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" /> Generating Quiz...
              </>
            ) : (
              <>
                <CloudUpload className="w-5 h-5" /> Generate Quiz
              </>
            )}
          </button>
        </form>

        {/* Message */}
        {message && (
          <p
            className={`mt-4 text-center font-medium ${
              message.startsWith("✅") ? "text-green-300" : "text-red-300"
            }`}
          >
            {message}
          </p>
        )}

        {/* Quiz Section */}
        {quizData && (
          <div className="mt-8 bg-white/10 p-6 rounded-2xl border border-white/20">
            <h2 className="text-2xl font-bold mb-4">📝 Generated Quiz</h2>
            {quizData.map((q, i) => (
              <div key={i} className="mb-6">
                <p className="font-semibold mb-2">{q.question}</p>
                {q.options.map((opt, j) => (
                  <label
                    key={j}
                    className="block mb-1 cursor-pointer hover:text-pink-200"
                  >
                    <input
                      type="radio"
                      name={`question-${i}`}
                      value={opt}
                      onChange={() => handleAnswerChange(i, opt)}
                      className="mr-2 accent-pink-400"
                    />
                    {opt}
                  </label>
                ))}
              </div>
            ))}

            <button
              onClick={handleEvaluate}
              className="mt-4 w-full bg-green-500 hover:bg-green-600 text-white font-semibold py-3 rounded-xl transition-all"
            >
              Submit Answers
            </button>
          </div>
        )}
      </div>

      <p className="text-white mt-6 text-sm opacity-80">
        © {new Date().getFullYear()} Adaptive Learning Platform
      </p>
    </div>
  );
};

export default UploadMaterial;

