import React, { useState } from 'react';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { api } from '../services/api';
import { GenerationRequest, TestType } from '../types';

const TestGenerator: React.FC = () => {
    const [loading, setLoading] = useState(false);
    const [generatedCode, setGeneratedCode] = useState<string | null>(null);
    const [error, setError] = useState<string | null>(null);

    const [formData, setFormData] = useState<GenerationRequest>({
        feature_description: '',
        test_type: TestType.UI,
        owner: 'qa_user',
        priority: 'normal',
        is_manual: true
    });

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setError(null);
        try {
            const result = await api.generateTestCase(formData);
            setGeneratedCode(result.code);
        } catch (err) {
            setError("Failed to generate test case. Ensure backend is running.");
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    const copyToClipboard = () => {
        if (generatedCode) {
            navigator.clipboard.writeText(generatedCode);
            alert("Copied to clipboard!");
        }
    };

    return (
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2rem' }}>
            {/* Left Column: Input */}
            <div className="card">
                <h2 style={{ marginBottom: '1.5rem', marginTop: 0 }}>Input Requirements</h2>
                <form onSubmit={handleSubmit}>
                    <div style={{ marginBottom: '1rem' }}>
                        <label>Feature Description & User Story</label>
                        <textarea
                            className="textarea"
                            rows={5}
                            placeholder="e.g. As a user I want to register via email..."
                            value={formData.feature_description}
                            onChange={(e) => setFormData({ ...formData, feature_description: e.target.value })}
                            required
                        />
                    </div>

                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
                        <div>
                            <label>Test Type</label>
                            <select
                                className="select"
                                value={formData.test_type}
                                onChange={(e) => setFormData({ ...formData, test_type: e.target.value as TestType })}
                            >
                                <option value={TestType.UI}>UI (Frontend)</option>
                                <option value={TestType.API}>API (Backend)</option>
                            </select>
                        </div>
                        <div>
                            <label>Generation Mode</label>
                            <select
                                className="select"
                                value={formData.is_manual ? 'manual' : 'auto'}
                                onChange={(e) => setFormData({ ...formData, is_manual: e.target.value === 'manual' })}
                            >
                                <option value="manual">Manual Test (Allure)</option>
                                <option value="auto">Autotest (Pytest)</option>
                            </select>
                        </div>
                    </div>

                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginTop: '1rem' }}>
                        <div>
                            <label>Owner</label>
                            <input
                                className="input"
                                type="text"
                                value={formData.owner}
                                onChange={(e) => setFormData({ ...formData, owner: e.target.value })}
                            />
                        </div>
                        <div>
                            <label>Priority</label>
                            <select
                                className="select"
                                value={formData.priority}
                                onChange={(e) => setFormData({ ...formData, priority: e.target.value })}
                            >
                                <option value="critical">Critical</option>
                                <option value="normal">Normal</option>
                                <option value="low">Low</option>
                            </select>
                        </div>
                    </div>

                    <button
                        type="submit"
                        className="btn btn-primary"
                        style={{ width: '100%', marginTop: '1.5rem', padding: '1rem' }}
                        disabled={loading}
                    >
                        {loading ? 'Generating...' : 'Generate Test Case'}
                    </button>
                    {error && <p style={{ color: '#ef4444', marginTop: '1rem' }}>{error}</p>}
                </form>
            </div>

            {/* Right Column: Output */}
            <div className="card" style={{ display: 'flex', flexDirection: 'column' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                    <h2 style={{ margin: 0 }}>Generated Code</h2>
                    {generatedCode && (
                        <button className="btn" style={{ backgroundColor: '#334155', color: 'white' }} onClick={copyToClipboard}>
                            Copy Code
                        </button>
                    )}
                </div>

                <div style={{ flex: 1, overflow: 'auto', borderRadius: '0.5rem', border: '1px solid #334155' }}>
                    {generatedCode ? (
                        <SyntaxHighlighter
                            language="python"
                            style={vscDarkPlus}
                            customStyle={{ margin: 0, height: '100%', borderRadius: 0 }}
                            showLineNumbers={true}
                        >
                            {generatedCode}
                        </SyntaxHighlighter>
                    ) : (
                        <div style={{ padding: '2rem', textAlign: 'center', color: '#64748b' }}>
                            Generated test case will appear here...
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default TestGenerator;
