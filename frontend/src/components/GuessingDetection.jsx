import React, { useEffect, useState } from "react";

/* ---------------- SHAP Bar Component ---------------- */
const Bar = ({ label, value, max = 1 }) => {
  const width = Math.min((value / max) * 100, 100);

  return (
    <div style={{ marginBottom: "8px" }}>
      <div style={{ fontSize: "14px", marginBottom: "2px" }}>
        {label}: <b>{value.toFixed(3)}</b>
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
            background: "#22c55e"
          }}
        />
      </div>
    </div>
  );
};

const GuessingDetection = () => {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch(
      "http://127.0.0.1:8000/api/agent/guessing-detection/student_123"
    )
      .then((res) => res.json())
      .then((result) => setData(result))
      .catch((err) => console.error(err));
  }, []);

  if (!data) return <p>Loading Guessing Detection...</p>;

  const analysis = data.guessing_detection_analysis;

  return (
    <div style={{ padding: "30px", maxWidth: "1000px", margin: "0 auto" }}>
      <h2 style={{ textAlign: "center", marginBottom: "10px" }}>
        Guessing & Overconfidence Detection (Explainable AI)
      </h2>

      <p style={{ textAlign: "center", marginBottom: "20px" }}>
        <b>Average Guessing Score:</b>{" "}
        {analysis.average_guessing_score.toFixed(3)} <br />
        <b>Average Overconfidence Score:</b>{" "}
        {analysis.average_overconfidence_score.toFixed(3)}
      </p>

      {analysis.questions.map((q, idx) => {
        const contributions = q.shap_explanation.features.map(
          (f) => f.contribution
        );
        const maxContribution = Math.max(...contributions);

        return (
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
            <h4>
              Q{idx + 1}. {q.question}
            </h4>

            <p>
              <b>Topic:</b> {q.topic}
            </p>

            <p>
              <b>Correct:</b>{" "}
              {q.is_correct ? "✅ Yes" : "❌ No"}
            </p>

            <p>
              <b>Guessing Score:</b> {q.guessing_score.toFixed(3)} <br />
              <b>Overconfidence Score:</b>{" "}
              {q.overconfidence_score.toFixed(3)}
            </p>

            {/* ---------------- SHAP EXPLANATION ---------------- */}
            <div style={{ marginTop: "15px" }}>
              <h5>SHAP Explanation (Why?)</h5>

              {q.shap_explanation.features.map((f, i) => (
                <Bar
                  key={i}
                  label={f.feature}
                  value={f.contribution}
                  max={maxContribution}
                />
              ))}
            </div>

            {/* ---------------- LIME EXPLANATION ---------------- */}
            <div style={{ marginTop: "20px" }}>
              <h5>LIME Explanation (What would reduce guessing?)</h5>

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
                      Impact
                    </th>
                    <th style={{ padding: "8px", border: "1px solid #ddd" }}>
                      Interpretation
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {q.lime_explanation.counterfactuals.map((cf, i) => (
                    <tr key={i}>
                      <td style={{ padding: "8px", border: "1px solid #ddd" }}>
                        {cf.feature}
                      </td>
                      <td style={{ padding: "8px", border: "1px solid #ddd" }}>
                        {cf.change}
                      </td>
                      <td style={{ padding: "8px", border: "1px solid #ddd" }}>
                        {cf.impact}
                      </td>
                      <td style={{ padding: "8px", border: "1px solid #ddd" }}>
                        {cf.interpretation}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        );
      })}
    </div>
  );
};

export default GuessingDetection;
