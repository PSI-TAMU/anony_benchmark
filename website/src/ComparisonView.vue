<template>
    <div class="min-vh-100 bg-white">
        <!-- Demo Section -->
        <div class="bg-white" id="demo">
            <div class="container py-5">
                <!-- Demo Header -->
                <div class="text-center mb-5">
                    <h2 class="demo-title">Interactive Demo</h2>
                    <p class="demo-subtitle">Compare voice conversion models across different tasks</p>
                </div>

                <!-- Model Selection -->
                <div class="row justify-content-center mb-5">
                    <div class="col-lg-10">
                        <div class="models-header">
                            <h3 class="models-title">Models</h3>
                            <button @click="addModel" class="btn-add-model"
                                :disabled="selectedModels.length >= availableModels.length">
                                <span>+ Add Model</span>
                            </button>
                        </div>

                        <div class="models-grid">
                            <div v-for="(model, index) in selectedModels" :key="index" class="model-card">
                                <div class="model-card-header">
                                    <div class="model-label">Model {{ String.fromCharCode(65 + index) }}</div>
                                    <button v-if="selectedModels.length > 1" @click="removeModel(index)"
                                        class="btn-remove-model">
                                        ×
                                    </button>
                                </div>
                                <select class="model-select" v-model="selectedModels[index]">
                                    <option v-for="availModel in availableModels" :key="availModel" :value="availModel">
                                        {{ availModel }}
                                    </option>
                                </select>
                            </div>
                        </div>
                    </div>
                </div>


                <!-- Task Selection Tabs -->
                <div class="row justify-content-center mb-5">
                    <div class="col-lg-10">
                        <div class="task-tabs-container">
                            <div class="task-tabs">
                                <button v-for="(config, taskKey) in taskConfigs" :key="taskKey"
                                    @click="selectedTask = taskKey"
                                    :class="['task-tab', { 'active': selectedTask === taskKey }]">
                                    {{ config.label }}
                                </button>
                            </div>
                            <div class="task-description">
                                <p class="mb-0">{{ taskConfigs[selectedTask].description }}</p>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Self-Reconstruction Layout -->
                <div v-if="selectedTask === 'self-recon'">
                    <!-- Utterance Selection -->
                    <div class="utterance-selector">
                        <label for="utteranceSelect" class="utterance-label">Select Utterance:</label>
                        <select id="utteranceSelect" v-model="selectedUtterance" class="utterance-select">
                            <option v-for="utterance in availableUtterances" :key="utterance" :value="utterance">
                                {{ utterance.replace('.wav', '') }}
                            </option>
                        </select>
                    </div>

                    <div class="reconstruction-layout">
                        <div v-for="(speaker, idx) in taskConfigs['self-recon'].speakers" :key="idx"
                            class="speaker-section">
                            <div class="speaker-title">{{ speaker.name }}</div>

                            <div class="audio-row"
                                :style="{ gridTemplateColumns: `repeat(${selectedModels.length + 1}, 1fr)` }">
                                <div class="audio-column">
                                    <div class="audio-label">Original</div>
                                    <audio :src="speaker.url" controls></audio>
                                </div>

                                <div v-for="(model, modelIdx) in selectedModels" :key="modelIdx" class="audio-column">
                                    <div class="audio-label">{{ model }}</div>
                                    <audio v-if="demoResults[idx]?.models?.[modelIdx]"
                                        :src="demoResults[idx].models[modelIdx]" controls></audio>
                                    <div v-else class="loading">Loading...</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Same-Utterance Layout -->
                <div v-else-if="selectedTask === 'same-utterance'" class="same-utterance-layout">
                    <!-- Speaker and Utterance Selectors -->
                    <div class="selector-panel">
                        <div class="selector-row">
                            <div class="selector-group">
                                <label class="selector-label">Speaker A (Source):</label>
                                <select v-model="selectedSpeakerA" class="speaker-select">
                                    <option v-for="speaker in sameUtteranceSpeakers" :key="speaker" :value="speaker">
                                        {{ speaker }}
                                    </option>
                                </select>
                            </div>

                            <div class="selector-group">
                                <label class="selector-label">Speaker B (Target):</label>
                                <select v-model="selectedSpeakerB" class="speaker-select">
                                    <option v-for="speaker in sameUtteranceSpeakers" :key="speaker" :value="speaker">
                                        {{ speaker }}
                                    </option>
                                </select>
                            </div>

                            <div class="selector-group">
                                <label class="selector-label">Utterance:</label>
                                <select v-model="selectedSameUtterance" class="utterance-select">
                                    <option v-for="utt in sameUtteranceUtterances" :key="utt" :value="utt">
                                        {{ utt.replace('.wav', '') }}
                                    </option>
                                </select>
                            </div>
                        </div>
                    </div>

                    <!-- Audio Display Section -->
                    <div class="same-utterance-section">
                        <div class="same-utterance-title">{{ selectedSpeakerA }} → {{ selectedSpeakerB }}</div>

                        <!-- Source and Target Row -->
                        <div class="audio-row" style="grid-template-columns: repeat(2, 1fr)">
                            <!-- Source Audio -->
                            <div class="audio-column">
                                <div class="audio-label">{{ selectedSpeakerA }} (Source)</div>
                                <audio :src="getAssetUrl(`/demo/original/${selectedSpeakerA}/${selectedSameUtterance}`)"
                                    controls></audio>
                            </div>

                            <!-- Target Audio -->
                            <div class="audio-column">
                                <div class="audio-label">{{ selectedSpeakerB }} (Target)</div>
                                <audio :src="getAssetUrl(`/demo/original/${selectedSpeakerB}/${selectedSameUtterance}`)"
                                    controls></audio>
                            </div>
                        </div>

                        <!-- Separator -->
                        <div class="results-separator"></div>

                        <!-- Model Results Row -->
                        <div class="results-row-container">
                            <div class="results-label">Converted Results:</div>
                            <div class="audio-row"
                                :style="{ gridTemplateColumns: `repeat(${selectedModels.length}, 1fr)` }">
                                <div v-for="(model, modelIdx) in selectedModels" :key="modelIdx" class="audio-column">
                                    <div class="audio-label">{{ model }}</div>
                                    <audio v-if="demoResults.sameUtterance?.models?.[modelIdx]"
                                        :src="demoResults.sameUtterance.models[modelIdx]" controls></audio>
                                    <div v-else class="loading">Loading...</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Full VC Layout -->
                <div v-else-if="selectedTask === 'full-vc'" class="same-utterance-layout">
                    <!-- Utterance Selectors -->
                    <div class="selector-panel">
                        <div class="selector-row">
                            <div class="selector-group">
                                <label class="selector-label">Source Utterance:</label>
                                <select v-model="selectedFullVCSourceUtterance" class="utterance-select">
                                    <option v-for="utt in fullVCSourceUtterances" :key="utt" :value="utt">
                                        {{ utt.replace('.wav', '') }}
                                    </option>
                                </select>
                            </div>

                            <div class="selector-group">
                                <label class="selector-label">Target Utterance:</label>
                                <select v-model="selectedFullVCTargetUtterance" class="utterance-select">
                                    <option v-for="utt in fullVCTargetUtterances" :key="utt" :value="utt">
                                        {{ utt.replace('.wav', '') }}
                                    </option>
                                </select>
                            </div>
                        </div>
                    </div>

                    <!-- Audio Display Section -->
                    <div class="same-utterance-section">
                        <div class="same-utterance-title">{{ selectedFullVCSourceUtterance.replace('.wav', '') }} → {{ selectedFullVCTargetUtterance.replace('.wav', '') }}</div>

                        <!-- Source and Target Row -->
                        <div class="audio-row" style="grid-template-columns: repeat(2, 1fr)">
                            <!-- Source Audio -->
                            <div class="audio-column">
                                <div class="audio-label">Source: {{ selectedFullVCSourceUtterance.replace('.wav', '') }}</div>
                                <audio :src="getAssetUrl(`/demo/full_vc/sources/${selectedFullVCSourceUtterance}`)"
                                    controls></audio>
                            </div>

                            <!-- Target Audio -->
                            <div class="audio-column">
                                <div class="audio-label">Target: {{ selectedFullVCTargetUtterance.replace('.wav', '') }}</div>
                                <audio :src="getAssetUrl(`/demo/full_vc/targets/${selectedFullVCTargetUtterance}`)"
                                    controls></audio>
                            </div>
                        </div>

                        <!-- Separator -->
                        <div class="results-separator"></div>

                        <!-- Model Results Row -->
                        <div class="results-row-container">
                            <div class="results-label">Converted Results:</div>
                            <div class="audio-row"
                                :style="{ gridTemplateColumns: `repeat(${selectedModels.length}, 1fr)` }">
                                <div v-for="(model, modelIdx) in selectedModels" :key="modelIdx" class="audio-column">
                                    <div class="audio-label">{{ model }}</div>
                                    <audio v-if="demoResults.fullVC?.models?.[modelIdx]"
                                        :src="demoResults.fullVC.models[modelIdx]" controls></audio>
                                    <div v-else class="loading">Loading...</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'

// Helper function to get the correct asset URL for GitHub Pages
const getAssetUrl = (path) => {
    const base = import.meta.env.BASE_URL || '/'
    // Remove leading slash from path and ensure base ends with slash
    const cleanPath = path.startsWith('/') ? path.slice(1) : path
    const cleanBase = base.endsWith('/') ? base : base + '/'
    return cleanBase + cleanPath
}

const availableModels = [
    'TVTSyn',
    'TVTSyn-m1-gtvt-diff-utt',
    'TVTSyn-m1-gtvt-same-utt',
    'TVTSyn-m1-gtvt-contrastive',
    'TVTSyn-m1-gtvt-ema',
]

// Selected models array (instead of just left/right)
const selectedModels = ref(['TVTSyn', 'TVTSyn-m1-gtvt-contrastive',  'TVTSyn-m1-gtvt-ema'])

// Add model
const addModel = () => {
    if (selectedModels.value.length < availableModels.length) {
        // Find first model not already selected
        const nextModel = availableModels.find(m => !selectedModels.value.includes(m))
        if (nextModel) {
            selectedModels.value.push(nextModel)
        }
    }
}

// Remove model
const removeModel = (index) => {
    if (selectedModels.value.length > 1) {
        selectedModels.value.splice(index, 1)
    }
}


// Task selection
const selectedTask = ref('self-recon') // 'self-recon', 'same-utterance', 'full-vc'

// Self-recon utterance selection
const availableUtterances = [
    'arctic_a0043.wav',
    'arctic_a0117.wav',
    'arctic_a0133.wav',
    'arctic_a0292.wav',
    'arctic_b0076.wav',
    'arctic_b0178.wav',
    'arctic_b0250.wav',
    'arctic_b0331.wav',
    'arctic_b0347.wav',
    'arctic_b0455.wav'
]
const selectedUtterance = ref(availableUtterances[0])

// Same-utterance selection
const sameUtteranceSpeakers = ['BDL', 'CLB', 'RMS', 'SLT']
const sameUtteranceUtterances = availableUtterances
const selectedSpeakerA = ref('BDL')
const selectedSpeakerB = ref('SLT')
const selectedSameUtterance = ref(availableUtterances[0])

// Full-VC selection (different utterances for source and target)
const fullVCSourceUtterances = ['BDL_arctic_a0406.wav', 'CLB_arctic_b0322.wav', 'MBMPS_arctic_b0244.wav', 'RRBI_arctic_a0055.wav', 'TNI_arctic_a0356.wav']
const fullVCTargetUtterances = ['ASI_arctic_a0292.wav', 'ERMS_arctic_a0113.wav', 'NJS_arctic_b0170.wav', 'SLT_arctic_a0334.wav', 'SVBI_arctic_a0508.wav']
const selectedFullVCSourceUtterance = ref(fullVCSourceUtterances[0])
const selectedFullVCTargetUtterance = ref(fullVCTargetUtterances[0])

// Demo mode data
const demoResults = ref({}) // Store results for each target-source combination

// Computed speakers for self-recon based on selected utterance
const getSelfReconSpeakers = () => {
    const speakers = ['BDL', 'CLB', 'RMS', 'SLT']
    return speakers.map(name => ({
        name,
        file: selectedUtterance.value,
        url: getAssetUrl(`/demo/original/${name}/${selectedUtterance.value}`)
    }))
}

// Task configurations
const taskConfigs = {
    'self-recon': {
        label: 'Self-Reconstruction',
        description: 'Models reconstruct the same speaker\'s voice',
        get speakers() {
            return getSelfReconSpeakers()
        }
    },
    'same-utterance': {
        label: 'VC (Same Utterance)',
        description: 'Different speakers, same content'
    },
    'full-vc': {
        label: 'Full VC',
        description: 'Different speakers, different content',
        sources: [
            { name: 'RRBI', url: getAssetUrl('/audio/demo/sources/RRBI_arctic_a0055.wav') },
            { name: 'TNI', url: getAssetUrl('/audio/demo/sources/TNI_arctic_a0356.wav') },
            { name: 'BDL', url: getAssetUrl('/audio/demo/sources/BDL_arctic_a0406.wav') },
            { name: 'MBMPS', url: getAssetUrl('/audio/demo/sources/MBMPS_arctic_b0244.wav') },
            { name: 'CLB', url: getAssetUrl('/audio/demo/sources/CLB_arctic_b0322.wav') }
        ],
        targets: [
            { name: 'ERMS', url: getAssetUrl('/audio/demo/targets/ERMS_arctic_a0113.wav') },
            { name: 'ASI', url: getAssetUrl('/audio/demo/targets/ASI_arctic_a0292.wav') },
            { name: 'SLT', url: getAssetUrl('/audio/demo/targets/SLT_arctic_a0334.wav') },
            { name: 'SVBI', url: getAssetUrl('/audio/demo/targets/SVBI_arctic_a0508.wav') },
            { name: 'NJS', url: getAssetUrl('/audio/demo/targets/NJS_arctic_b0170.wav') }
        ]
    }
}

// Generate all demo combinations at once
const generateAllDemoVC = async () => {
    try {
        const newResults = {}

        if (selectedTask.value === 'self-recon') {
            // Self-reconstruction: simpler structure
            const speakers = taskConfigs['self-recon'].speakers
            for (let idx = 0; idx < speakers.length; idx++) {
                const speaker = speakers[idx]
                const models = []

                // Generate URL for each selected model
                // Path: /demo/vc_same_utt/{model}/{speaker}/{speaker}/{utterance}.wav
                for (let modelIdx = 0; modelIdx < selectedModels.value.length; modelIdx++) {
                    const modelName = selectedModels.value[modelIdx]
                    models.push(getAssetUrl(`/demo/vc_same_utt/${modelName}/${speaker.name}/${speaker.name}/${speaker.file}`))
                }

                newResults[idx] = { models }
            }
        } else if (selectedTask.value === 'same-utterance') {
            // Selector-based layout for same-utterance
            const models = []

            // Generate URL for each selected model
            // Path: /demo/vc_same_utt/{model}/{source}/{target}/{utterance}.wav
            for (let modelIdx = 0; modelIdx < selectedModels.value.length; modelIdx++) {
                const modelName = selectedModels.value[modelIdx]

                const resultPath = `/demo/vc_same_utt/${modelName}/${selectedSpeakerA.value}/${selectedSpeakerB.value}/${selectedSameUtterance.value}`
                models.push(getAssetUrl(resultPath))
            }

            newResults.sameUtterance = { models }
        } else if (selectedTask.value === 'full-vc') {
            // Selector-based layout for full-vc with different utterances
            const models = []

            // Generate URL for each selected model
            // Path: /demo/full_vc/models/{model}/{target_utt}/{source_utt}.wav
            for (let modelIdx = 0; modelIdx < selectedModels.value.length; modelIdx++) {
                const modelName = selectedModels.value[modelIdx]
                const targetUtt = selectedFullVCTargetUtterance.value.replace('.wav', '')
                const sourceUtt = selectedFullVCSourceUtterance.value

                const resultPath = `/demo/full_vc/models/${modelName}/${targetUtt}/${sourceUtt}`
                models.push(getAssetUrl(resultPath))
            }

            newResults.fullVC = { models }
        }

        demoResults.value = newResults

    } catch (error) {
        console.error('Batch voice conversion failed:', error)
    }
}

// Watch for model changes and regenerate demo results
watch(selectedModels, () => {
    // Only regenerate if we have existing results
    if (Object.keys(demoResults.value).length > 0) {
        generateAllDemoVC()
    }
}, { deep: true })

// Watch for task changes and regenerate demo results
watch(selectedTask, () => {
    generateAllDemoVC()
})

// Watch for utterance changes in self-recon
watch(selectedUtterance, () => {
    if (selectedTask.value === 'self-recon') {
        generateAllDemoVC()
    }
})

// Watch for speaker and utterance changes in same-utterance
watch([selectedSpeakerA, selectedSpeakerB, selectedSameUtterance], () => {
    if (selectedTask.value === 'same-utterance') {
        generateAllDemoVC()
    }
})

// Watch for utterance changes in full-vc
watch([selectedFullVCSourceUtterance, selectedFullVCTargetUtterance], () => {
    if (selectedTask.value === 'full-vc') {
        generateAllDemoVC()
    }
})

// Generate demo results when component mounts
onMounted(() => {
    // Auto-generate demo results on page load
    generateAllDemoVC()
})
</script>

<style scoped>
/* Demo Header */
.demo-title {
    font-size: 36px;
    font-weight: 700;
    color: #24292f;
    letter-spacing: -1px;
    margin-bottom: 8px;
    background: linear-gradient(135deg, #24292f 0%, #0969da 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.demo-subtitle {
    font-size: 16px;
    font-weight: 400;
    color: #57606a;
    letter-spacing: -0.2px;
    line-height: 1.4;
    margin: 0;
}

/* Model Selection */
.models-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}

.models-title {
    font-size: 20px;
    font-weight: 600;
    color: #24292f;
    margin: 0;
    letter-spacing: -0.3px;
}

.btn-add-model {
    padding: 8px 16px;
    background: #0969da;
    color: #ffffff;
    border: none;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
    letter-spacing: -0.1px;
}

.btn-add-model:hover:not(:disabled) {
    background: #0550ae;
    transform: translateY(-1px);
    box-shadow: 0 2px 8px rgba(9, 105, 218, 0.3);
}

.btn-add-model:disabled {
    background: #d0d7de;
    cursor: not-allowed;
    opacity: 0.6;
}

.models-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 16px;
}

/* Model Selection Cards */
.model-card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
}

.btn-remove-model {
    width: 24px;
    height: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: transparent;
    border: 1px solid #d0d7de;
    border-radius: 6px;
    color: #57606a;
    font-size: 18px;
    line-height: 1;
    cursor: pointer;
    transition: all 0.2s ease;
    padding: 0;
}

.btn-remove-model:hover {
    background: #ff4444;
    border-color: #ff4444;
    color: #ffffff;
}

/* Model Selection Cards */
.model-card {
    background: #ffffff;
    border: 1px solid #e1e4e8;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
    transition: all 0.3s ease;
}

.model-card:hover {
    border-color: #c9d1d9;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    transform: translateY(-2px);
}

.model-label {
    font-size: 11px;
    font-weight: 600;
    color: #57606a;
    margin-bottom: 10px;
    letter-spacing: 0.3px;
    text-transform: uppercase;
}

.model-select {
    width: 100%;
    padding: 12px 14px;
    font-size: 15px;
    border: 1.5px solid #d0d7de;
    border-radius: 8px;
    background: #ffffff;
    color: #24292f;
    font-weight: 500;
    letter-spacing: -0.2px;
    transition: all 0.2s ease;
}

.model-select:focus {
    outline: none;
    border-color: #0969da;
    box-shadow: 0 0 0 3px rgba(9, 105, 218, 0.1);
}

.model-select:hover {
    border-color: #57606a;
}

/* Task Tabs */
.task-tabs-container {
    background: #ffffff;
    border: 1px solid #e1e4e8;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
}

.task-tabs {
    display: flex;
    border-bottom: 1px solid #e1e4e8;
    background: #f6f8fa;
}

.task-tab {
    flex: 1;
    padding: 14px 20px;
    background: transparent;
    border: none;
    font-size: 15px;
    font-weight: 500;
    color: #57606a;
    cursor: pointer;
    position: relative;
    letter-spacing: -0.2px;
    transition: all 0.2s ease;
}

.task-tab:hover {
    color: #24292f;
    background: rgba(0, 0, 0, 0.02);
}

.task-tab.active {
    color: #24292f;
    font-weight: 600;
    background: #ffffff;
}

.task-tab.active::after {
    content: '';
    position: absolute;
    bottom: -1px;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, #0969da 0%, #0550ae 100%);
    border-radius: 3px 3px 0 0;
}

.task-description {
    padding: 16px 20px;
    text-align: center;
    color: #57606a;
    font-size: 14px;
    line-height: 1.5;
    letter-spacing: -0.1px;
}

/* ==========================================
   RECONSTRUCTION LAYOUT
   ========================================== */
.utterance-selector {
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 32px;
    padding: 20px;
    background: #ffffff;
    border: 1px solid #e1e4e8;
    border-radius: 12px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
}

.utterance-label {
    font-size: 14px;
    font-weight: 600;
    color: #24292f;
    letter-spacing: -0.2px;
    white-space: nowrap;
}

.utterance-select {
    flex: 1;
    max-width: 300px;
    padding: 12px 14px;
    font-size: 15px;
    border: 1.5px solid #d0d7de;
    border-radius: 8px;
    background: #ffffff;
    color: #24292f;
    font-weight: 500;
    letter-spacing: -0.2px;
    transition: all 0.2s ease;
}

.utterance-select:focus {
    outline: none;
    border-color: #0969da;
    box-shadow: 0 0 0 3px rgba(9, 105, 218, 0.1);
}

.utterance-select:hover {
    border-color: #57606a;
}

.reconstruction-layout {
    display: flex;
    flex-direction: column;
    gap: 24px;
}

.speaker-section {
    background: #ffffff;
    border: 1px solid #e1e4e8;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
    transition: all 0.3s ease;
}

.speaker-section:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.speaker-title {
    font-size: 19px;
    font-weight: 600;
    color: #24292f;
    margin-bottom: 16px;
    letter-spacing: -0.4px;
    padding-bottom: 12px;
    border-bottom: 2px solid #f6f8fa;
}

.audio-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
}

.audio-column {
    display: flex;
    flex-direction: column;
    gap: 10px;
    background: #f6f8fa;
    padding: 14px;
    border-radius: 10px;
    border: 1px solid #e1e4e8;
    transition: all 0.2s ease;
}

.audio-column:hover {
    background: #ffffff;
    border-color: #c9d1d9;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.audio-label {
    font-size: 11px;
    font-weight: 600;
    color: #57606a;
    letter-spacing: 0.3px;
    text-transform: uppercase;
}

.audio-column audio {
    width: 100%;
    height: 40px;
    outline: none;
}

/* ==========================================
   SAME-UTTERANCE SELECTOR LAYOUT
   ========================================== */
.same-utterance-layout {
    display: flex;
    flex-direction: column;
    gap: 24px;
}

.selector-panel {
    background: #ffffff;
    border: 1px solid #e1e4e8;
    border-radius: 12px;
    padding: 24px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
}

.selector-row {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 20px;
}

.selector-group {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.selector-label {
    font-size: 13px;
    font-weight: 600;
    color: #24292f;
    letter-spacing: -0.2px;
}

.speaker-select,
.utterance-select {
    width: 100%;
    padding: 12px 14px;
    font-size: 15px;
    border: 1.5px solid #d0d7de;
    border-radius: 8px;
    background: #ffffff;
    color: #24292f;
    font-weight: 500;
    letter-spacing: -0.2px;
    transition: all 0.2s ease;
}

.speaker-select:focus,
.utterance-select:focus {
    outline: none;
    border-color: #0969da;
    box-shadow: 0 0 0 3px rgba(9, 105, 218, 0.1);
}

.speaker-select:hover,
.utterance-select:hover {
    border-color: #57606a;
}

.same-utterance-section {
    background: #ffffff;
    border: 1px solid #e1e4e8;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
    transition: all 0.3s ease;
}

.same-utterance-section:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.same-utterance-title {
    font-size: 19px;
    font-weight: 600;
    color: #24292f;
    margin-bottom: 16px;
    letter-spacing: -0.4px;
    padding-bottom: 12px;
    border-bottom: 2px solid #f6f8fa;
}

.results-separator {
    height: 1px;
    background: linear-gradient(to right, transparent, #d0d7de 20%, #d0d7de 80%, transparent);
    margin: 24px 0;
    position: relative;
}

.results-separator::before {
    content: '';
    position: absolute;
    top: -4px;
    left: 50%;
    transform: translateX(-50%);
    width: 8px;
    height: 8px;
    background: #0969da;
    border-radius: 50%;
    box-shadow: 0 0 0 3px #ffffff, 0 0 0 4px #d0d7de;
}

.results-row-container {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.results-label {
    font-size: 14px;
    font-weight: 600;
    color: #57606a;
    letter-spacing: -0.2px;
    text-transform: uppercase;
    font-size: 12px;
    letter-spacing: 0.5px;
}

/* ==========================================
   VC LAYOUT
   ========================================== */
.vc-layout {
    overflow-x: auto;
    background: #ffffff;
    border: 1px solid #e1e4e8;
    border-radius: 12px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
}

.vc-table {
    display: inline-block;
    min-width: 100%;
}

.vc-header-row,
.vc-data-row {
    display: grid;
    grid-template-columns: 150px repeat(5, minmax(220px, 1fr));
    border-bottom: 1px solid #e1e4e8;
}

.vc-header-row {
    background: #f6f8fa;
}

.vc-data-row:last-child {
    border-bottom: none;
}

.vc-corner,
.vc-source-cell,
.vc-target-cell,
.vc-result-cell {
    padding: 16px;
}

.vc-source-cell,
.vc-target-cell {
    display: flex;
    flex-direction: column;
    gap: 10px;
    transition: all 0.2s ease;
}

.vc-source-cell:hover,
.vc-target-cell:hover {
    background: rgba(9, 105, 218, 0.03);
}

.cell-label {
    font-size: 14px;
    font-weight: 600;
    color: #24292f;
    letter-spacing: -0.3px;
}

.vc-source-cell audio,
.vc-target-cell audio {
    width: 100%;
    height: 36px;
    outline: none;
}

.vc-result-cell {
    background: #ffffff;
    transition: all 0.2s ease;
}

.vc-result-cell:hover {
    background: #fafbfc;
}

.result-content {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.result-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px;
    background: #f6f8fa;
    border-radius: 8px;
    border: 1px solid #e1e4e8;
    transition: all 0.2s ease;
}

.result-item:hover {
    background: #ffffff;
    border-color: #c9d1d9;
}

.result-label {
    font-size: 12px;
    font-weight: 600;
    color: #57606a;
    min-width: 22px;
    height: 22px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #ffffff;
    border-radius: 6px;
    border: 1.5px solid #d0d7de;
}

.result-item audio {
    width: 100%;
    height: 32px;
    outline: none;
}

/* ==========================================
   LOADING STATE
   ========================================== */
.loading {
    color: #57606a;
    font-size: 13px;
    font-weight: 500;
    padding: 16px 0;
    text-align: center;
    font-style: italic;
}

/* Responsive Adjustments */
@media (max-width: 1024px) {

    .vc-header-row,
    .vc-data-row {
        grid-template-columns: 140px repeat(5, minmax(200px, 1fr));
    }

    .audio-row {
        gap: 14px;
    }

    .same-utterance-section {
        padding: 16px;
    }
}

@media (max-width: 768px) {
    .demo-title {
        font-size: 28px;
        letter-spacing: -0.7px;
    }

    .demo-subtitle {
        font-size: 15px;
    }

    .task-tab {
        font-size: 14px;
        padding: 12px 16px;
    }

    .model-card {
        padding: 16px;
    }

    .utterance-selector {
        flex-direction: column;
        align-items: flex-start;
        gap: 12px;
        padding: 16px;
        margin-bottom: 24px;
    }

    .utterance-select {
        max-width: 100%;
        width: 100%;
    }

    .speaker-section {
        padding: 16px;
    }

    .speaker-title {
        font-size: 17px;
        margin-bottom: 12px;
        padding-bottom: 10px;
    }

    .audio-row {
        grid-template-columns: 1fr;
        gap: 12px;
    }

    .audio-column {
        padding: 12px;
    }

    .vc-header-row,
    .vc-data-row {
        grid-template-columns: 120px repeat(5, minmax(180px, 1fr));
    }

    .vc-corner,
    .vc-source-cell,
    .vc-target-cell,
    .vc-result-cell {
        padding: 12px;
    }

    .cell-label {
        font-size: 13px;
    }

    .result-item {
        padding: 8px;
        gap: 8px;
    }

    .selector-row {
        grid-template-columns: 1fr;
        gap: 16px;
    }

    .selector-panel {
        padding: 16px;
    }

    .same-utterance-section {
        padding: 16px;
    }

    .same-utterance-title {
        font-size: 17px;
    }

    .results-separator {
        margin: 20px 0;
    }

    .results-label {
        font-size: 11px;
    }
}
</style>
