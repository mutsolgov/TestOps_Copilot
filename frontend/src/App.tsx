import TestGenerator from './components/TestGenerator';

function App() {
    return (
        <div className="container">
            <header className="header">
                <h1>TestOps Copilot AI</h1>
                <p style={{ color: '#94a3b8', margin: '0.5rem 0 0' }}>
                    Automated QA Assistant powered by Cloud.ru Evolution
                </p>
            </header>
            <main>
                <TestGenerator />
            </main>
        </div>
    );
}

export default App;
