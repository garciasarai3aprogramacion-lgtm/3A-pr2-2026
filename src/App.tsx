import { useState } from "react";
import { Calculator, Delete } from "lucide-react";
import { Route, Router as WouterRouter, Switch } from "wouter";

function Home() {
  const [numero1, setNumero1] = useState("");
  const [numero2, setNumero2] = useState("");
  const [resultado, setResultado] = useState("Resultado: 0");
  const [error, setError] = useState(false);

  const sumar = () => {
    const first = Number(numero1);
    const second = Number(numero2);

    if (numero1.trim() === "" || numero2.trim() === "" || !Number.isFinite(first) || !Number.isFinite(second)) {
      setResultado("Ingresa números válidos");
      setError(true);
      return;
    }

    setResultado(`Resultado: ${first + second}`);
    setError(false);
  };

  const limpiar = () => {
    setNumero1("");
    setNumero2("");
    setResultado("Resultado: 0");
    setError(false);
  };

  return (
    <main className="sum-page">
      <div className="sum-orb sum-orb-one" aria-hidden="true" />
      <div className="sum-orb sum-orb-two" aria-hidden="true" />
      <section className="sum-card" aria-labelledby="page-title">
        <div className="sum-card-header">
          <div className="sum-icon" aria-hidden="true">
            <Calculator size={22} strokeWidth={2.4} />
          </div>
          <div>
            <p className="sum-kicker">Python + NiceGUI</p>
            <h1 id="page-title">Calculadora de Suma</h1>
          </div>
        </div>

        <p className="sum-description">
          Ingresa dos números y obtén el resultado de forma rápida.
        </p>

        <div className="sum-form">
          <label htmlFor="numero1">Número 1</label>
          <input
            id="numero1"
            inputMode="decimal"
            value={numero1}
            onChange={(event) => setNumero1(event.target.value)}
            placeholder="Ej. 12.5"
          />

          <label htmlFor="numero2">Número 2</label>
          <input
            id="numero2"
            inputMode="decimal"
            value={numero2}
            onChange={(event) => setNumero2(event.target.value)}
            placeholder="Ej. 7.5"
            onKeyDown={(event) => {
              if (event.key === "Enter") sumar();
            }}
          />
        </div>

        <div className="sum-actions">
          <button type="button" className="sum-button sum-button-primary" onClick={sumar}>
            <Calculator size={18} />
            SUMAR
          </button>
          <button type="button" className="sum-button sum-button-secondary" onClick={limpiar}>
            <Delete size={18} />
            LIMPIAR
          </button>
        </div>

        <div className={`sum-result ${error ? "sum-result-error" : ""}`} role="status">
          {resultado}
        </div>

        <p className="sum-footer">Proyecto de programación · Listo para practicar</p>
      </section>
    </main>
  );
}

function App() {
  return (
    <WouterRouter base={import.meta.env.BASE_URL.replace(/\/$/, "")}>
      <Switch>
        <Route path="/" component={Home} />
      </Switch>
    </WouterRouter>
  );
}

export default App;