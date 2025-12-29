// import React, { useEffect, useState } from "react";

// /* ---------------- SHAP Bar Component ---------------- */
// const Bar = ({ label, value, max = 1 }) => {
//   const width = Math.min((value / max) * 100, 100);

//   return (
//     <div style={{ marginBottom: "8px" }}>
//       <div style={{ fontSize: "14px", marginBottom: "2px" }}>
//         {label}: <b>{value}</b>
//       </div>
//       <div
//         style={{
//           height: "10px",
//           background: "#eee",
//           borderRadius: "6px",
//           overflow: "hidden"
//         }}
//       >
//         <div
//           style={{
//             width: `${width}%`,
//             height: "100%",
//             background: "#4f46e5"
//           }}
//         />
//       </div>
//     </div>
//   );
// };

// /* ---------------- Main Component ---------------- */
// const ConceptMasteryConfidence = () => {
//   const [data, setData] = useState(null);

//   useEffect(() => {
//     fetch(
//       "http://127.0.0.1:8000/api/agent/concept_mastery_confidence/student_123"
//     )
//       .then((res) => res.json())
//       .then((result) => setData(result))
//       .catch((err) => console.error(err));
//   }, []);

//   if (!data) return <p>Loading Concept Mastery Confidence...</p>;

//   const concepts = data.concept_mastery_confidence.concepts;

//   return (
//     <div style={{ padding: "30px", maxWidth: "900px", margin: "0 auto" }}>
//       <h2 style={{ textAlign: "center", marginBottom: "30px" }}>
//         Concept Mastery Confidence (Explainable AI)
//       </h2>

//       {concepts.map((c, idx) => (
//         <div
//           key={idx}
//           style={{
//             background: "#ffffff",
//             color: "#000",
//             padding: "20px",
//             marginBottom: "20px",
//             borderRadius: "10px",
//             boxShadow: "0 4px 10px rgba(0,0,0,0.15)"
//           }}
//         >
//           <h3>{c.concept}</h3>

//           <p>
//             <b>Confidence Score:</b> {c.confidence_score}
//           </p>
//           <p>
//             <b>Mastery Level:</b> {c.mastery_level}
//           </p>

//           {/* ---------------- SHAP EXPLANATION ---------------- */}
//           <div style={{ marginTop: "15px" }}>
//             <h4>SHAP Explanation (Why this score?)</h4>

//             {c.shap_explanation.features.map((f, i) => (
//               <Bar
//                 key={i}
//                 label={f.feature}
//                 value={f.contribution}
//                 max={1}
//               />
//             ))}
//           </div>

//           {/* ---------------- LIME EXPLANATION ---------------- */}
//           <div style={{ marginTop: "20px" }}>
//             <h4>LIME Explanation (What would change?)</h4>

//             <table
//               style={{
//                 width: "100%",
//                 borderCollapse: "collapse",
//                 marginTop: "10px",
//                 fontSize: "14px"
//               }}
//             >
//               <thead>
//                 <tr style={{ background: "#f3f4f6" }}>
//                   <th style={{ padding: "8px", border: "1px solid #ddd" }}>
//                     Feature
//                   </th>
//                   <th style={{ padding: "8px", border: "1px solid #ddd" }}>
//                     Change
//                   </th>
//                   <th style={{ padding: "8px", border: "1px solid #ddd" }}>
//                     Confidence Impact
//                   </th>
//                   <th style={{ padding: "8px", border: "1px solid #ddd" }}>
//                     Interpretation
//                   </th>
//                 </tr>
//               </thead>
//               <tbody>
//                 {c.lime_explanation.counterfactuals.map((cf, i) => (
//                   <tr key={i}>
//                     <td
//                       style={{ padding: "8px", border: "1px solid #ddd" }}
//                     >
//                       {cf.feature}
//                     </td>
//                     <td
//                       style={{ padding: "8px", border: "1px solid #ddd" }}
//                     >
//                       {cf.change}
//                     </td>
//                     <td
//                       style={{
//                         padding: "8px",
//                         border: "1px solid #ddd",
//                         color: cf.confidence_change.startsWith("+")
//                           ? "green"
//                           : "red"
//                       }}
//                     >
//                       {cf.confidence_change}
//                     </td>
//                     <td
//                       style={{ padding: "8px", border: "1px solid #ddd" }}
//                     >
//                       {cf.interpretation}
//                     </td>
//                   </tr>
//                 ))}
//               </tbody>
//             </table>
//           </div>
//         </div>
//       ))}
//     </div>
//   );
// };

// export default ConceptMasteryConfidence;

import React, { useEffect, useState } from "react";

/* ---------------- SHAP Bar Component ---------------- */
const Bar = ({ label, value, max = 1 }) => {
  const width = Math.min((value / max) * 100, 100);

  return (
    <div style={{ marginBottom: "8px" }}>
      <div style={{ fontSize: "14px", marginBottom: "2px" }}>
        {label}: <b>{value}</b>
      </div>
      <div
        style={{
          height: "10px",
          background: "#eee",
          borderRadius: "6px",
          overflow: "hidden"
        }}
      >
        <div
          style={{
            width: `${width}%`,
            height: "100%",
            background: "#4f46e5"
          }}
        />
      </div>
    </div>
  );
};

/* ---------------- Main Component ---------------- */
const ConceptMasteryConfidence = () => {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch(
      "http://127.0.0.1:8000/api/agent/concept_mastery_confidence/student_123"
    )
      .then((res) => res.json())
      .then((result) => setData(result))
      .catch((err) => console.error(err));
  }, []);

  if (!data) return <p>Loading Concept Mastery Confidence...</p>;

  const concepts = data?.concept_mastery_confidence?.concepts || [];

  return (
    <div style={{ padding: "30px", maxWidth: "900px", margin: "0 auto" }}>
      <h2 style={{ textAlign: "center", marginBottom: "30px" }}>
        Concept Mastery Confidence (Explainable AI)
      </h2>

      {concepts.map((c, idx) => (
        <div
          key={idx}
          style={{
            background: "#ffffff",
            color: "#000",
            padding: "20px",
            marginBottom: "20px",
            borderRadius: "10px",
            boxShadow: "0 4px 10px rgba(0,0,0,0.15)"
          }}
        >
          <h3>{c.concept}</h3>

          <p>
            <b>Confidence Score:</b> {c.confidence_score}
          </p>
          <p>
            <b>Mastery Level:</b> {c.mastery_level}
          </p>

          {/* ---------------- SHAP EXPLANATION ---------------- */}
          {c.shap_explanation?.features && (
            <div style={{ marginTop: "15px" }}>
              <h4>SHAP Explanation (Why this score?)</h4>

              {c.shap_explanation.features.map((f, i) => (
                <Bar
                  key={i}
                  label={f.feature}
                  value={f.contribution}
                  max={1}
                />
              ))}
            </div>
          )}

          {/* ---------------- LIME EXPLANATION ---------------- */}
          {c.lime_explanation?.counterfactuals && (
            <div style={{ marginTop: "20px" }}>
              <h4>LIME Explanation (What would change?)</h4>

              <table
                style={{
                  width: "100%",
                  borderCollapse: "collapse",
                  marginTop: "10px",
                  fontSize: "14px"
                }}
              >
                <thead>
                  <tr style={{ background: "#f3f4f6" }}>
                    <th style={{ padding: "8px", border: "1px solid #ddd" }}>
                      Feature
                    </th>
                    <th style={{ padding: "8px", border: "1px solid #ddd" }}>
                      Change
                    </th>
                    <th style={{ padding: "8px", border: "1px solid #ddd" }}>
                      Confidence Impact
                    </th>
                    <th style={{ padding: "8px", border: "1px solid #ddd" }}>
                      Interpretation
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {c.lime_explanation.counterfactuals.map((cf, i) => (
                    <tr key={i}>
                      <td style={{ padding: "8px", border: "1px solid #ddd" }}>
                        {cf.feature}
                      </td>
                      <td style={{ padding: "8px", border: "1px solid #ddd" }}>
                        {cf.change}
                      </td>
                      <td
                        style={{
                          padding: "8px",
                          border: "1px solid #ddd",
                          color: cf.confidence_change.startsWith("+")
                            ? "green"
                            : "red"
                        }}
                      >
                        {cf.confidence_change}
                      </td>
                      <td style={{ padding: "8px", border: "1px solid #ddd" }}>
                        {cf.interpretation}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      ))}
    </div>
  );
};

export default ConceptMasteryConfidence;
