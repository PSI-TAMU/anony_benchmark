<template>
    <div class="min-vh-100 bg-white">
        <!-- Paper Header -->
        <div class="border-bottom">
            <div class="container py-5">
                <div class="text-center">
                    <!-- Paper Title -->
                    <h1 class="display-5 fw-light text-black mb-4 lh-base"
                        style="font-weight: 300; letter-spacing: -1px;">
                        Content-Synchronous Time-Varying Timbre<br>
                        <span class="fw-bold">for Streaming Voice Anonymization</span>
                    </h1>

                    <!-- Conference Info -->
                    <div class="mb-5">
                        <p class="text-black fs-6 mb-0">Anonymized submission for ICLR 2026</p>
                    </div>

                    <!-- Abstract -->
                    <div class="row justify-content-center">
                        <div class="col-lg-9">
                            <div class="text-start">
                                <h2 class="h6 fw-bold text-uppercase text-black mb-3 tracking-wide"
                                    style="letter-spacing: 2px;">Abstract</h2>
                                <p class="text-black lh-lg mb-0" style="font-size: 1.1rem; font-weight: 400;">
                                    Real-time voice conversion and speech anonymization require causal, low-latency
                                    synthesis without sacrificing intelligibility or naturalness. A core limitation of
                                    current systems is a representational mismatch: content is time-varying, while
                                    speaker
                                    identity is injected as a static global embedding, yielding over-smoothed timbre and
                                    reduced expressivity. We introduce a streamable speech synthesizer that aligns the
                                    temporal granularity of identity and content via a <strong>content-synchronous,
                                        time-varying
                                        timbre representation</strong>. A Global Timbre Memory expands a global timbre
                                    seed into compact
                                    facets; frame-level content attends to this memory, a gate regulates variation, and
                                    spherical interpolation preserves identity geometry while enabling smooth local
                                    changes.
                                    Complementing this, a factorized vector-quantized bottleneck regularizes content to
                                    reduce residual speaker leakage. The resulting system is fully streamable, with
                                    <strong>&lt;80 ms
                                        GPU latency</strong>. Experiments demonstrate improvements in naturalness,
                                    speaker
                                    similarity, and anonymization strength compared to state-of-the-art streaming
                                    baselines, establishing TVT as a scalable approach for privacy-preserving and
                                    expressive speech synthesis under strict latency budgets.
                                </p>
                            </div>
                        </div>
                    </div>

                    <!-- Links -->
                    <div class="mt-5">
                        <a href="#" class="btn btn-outline-dark me-3 px-4 py-2">Paper</a>
                        <a href="#" class="btn btn-dark me-3 px-4 py-2">Code</a>
                        <a href="#demo" class="btn btn-outline-dark px-4 py-2">Demo ↓</a>
                    </div>
                </div>
            </div>
        </div>

        <!-- Demo Section -->
        <div class="bg-white" id="demo">
            <div class="container py-5">
                <!-- Demo Header -->
                <div class="text-center mb-5">
                    <h2 class="h3 fw-light text-black mb-3" style="letter-spacing: -0.5px;">Interactive Demo</h2>
                    <p class="text-black-50 mb-0">Compare voice conversion models across source and target speakers</p>
                </div>

                <!-- Model Selection -->
                <div class="row justify-content-center mb-5">
                    <div class="col-lg-10">
                        <div class="row">
                            <div class="col-md-6 mb-4">
                                <div class="border p-4">
                                    <h4 class="h6 fw-bold text-uppercase mb-3 text-black" style="letter-spacing: 1px;">
                                        Model A</h4>
                                    <select id="leftModel" class="form-select form-select-lg border-dark mb-3"
                                        v-model="leftModel">
                                        <option v-for="model in availableModels" :key="model" :value="model">{{ model }}
                                        </option>
                                    </select>
                                    <div class="d-flex justify-content-between text-black-50">
                                        <div class="text-center">
                                            <div class="fw-bold text-black">{{ modelInfos[leftModel].latency }}</div>
                                            <small>Latency</small>
                                        </div>
                                        <div class="text-center">
                                            <div class="fw-bold text-black">{{ modelInfos[leftModel].rtf }}</div>
                                            <small>RTF</small>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-6 mb-4">
                                <div class="border p-4">
                                    <h4 class="h6 fw-bold text-uppercase mb-3 text-black" style="letter-spacing: 1px;">
                                        Model B</h4>
                                    <select id="rightModel" class="form-select form-select-lg border-dark mb-3"
                                        v-model="rightModel">
                                        <option v-for="model in availableModels" :key="model" :value="model">{{ model }}
                                        </option>
                                    </select>
                                    <div class="d-flex justify-content-between text-black-50">
                                        <div class="text-center">
                                            <div class="fw-bold text-black">{{ modelInfos[rightModel].latency }}</div>
                                            <small>Latency</small>
                                        </div>
                                        <div class="text-center">
                                            <div class="fw-bold text-black">{{ modelInfos[rightModel].rtf }}</div>
                                            <small>RTF</small>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Upload Mode Content -->
                <div v-if="currentMode === 'upload'">
                    <!-- Audio Upload Section -->
                    <div class="row mb-4">
                        <div class="col-md-6">
                            <div class="card">
                                <div class="card-body">
                                    <h5 class="card-title">Source Audio</h5>
                                    <input type="file" class="form-control mb-3" accept="audio/*"
                                        @change="handleSourceUpload">
                                    <audio v-if="sourceAudioUrl" :src="sourceAudioUrl" controls class="w-100"></audio>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="card">
                                <div class="card-body">
                                    <h5 class="card-title">Target Audio</h5>
                                    <input type="file" class="form-control mb-3" accept="audio/*"
                                        @change="handleTargetUpload">
                                    <audio v-if="targetAudioUrl" :src="targetAudioUrl" controls class="w-100"></audio>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Voice Conversion Results -->
                    <div class="row g-4" v-if="sourceAudioUrl && targetAudioUrl">
                        <div class="col-md-6">
                            <div class="card shadow-sm h-100">
                                <div class="card-body">
                                    <h2 class="card-title fw-semibold mb-3">{{ leftModel }}</h2>
                                    <div class="mb-3">
                                        <button class="btn btn-primary" @click="performVC('left')"
                                            :disabled="isProcessing">
                                            {{ isProcessing ? 'Processing...' : 'Generate Voice Conversion' }}
                                        </button>
                                    </div>
                                    <audio v-if="leftResult" :src="leftResult" controls class="w-100"></audio>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="card shadow-sm h-100">
                                <div class="card-body">
                                    <h2 class="card-title fw-semibold mb-3">{{ rightModel }}</h2>
                                    <div class="mb-3">
                                        <button class="btn btn-primary" @click="performVC('right')"
                                            :disabled="isProcessing">
                                            {{ isProcessing ? 'Processing...' : 'Generate Voice Conversion' }}
                                        </button>
                                    </div>
                                    <audio v-if="rightResult" :src="rightResult" controls class="w-100"></audio>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Demo Results Table -->
                <div v-else>
                    <div class="table-responsive">
                        <table class="table table-bordered align-middle border-dark">
                            <thead class="border-dark">
                                <tr>
                                    <th class="bg-black text-white text-center fw-normal py-3"
                                        style="min-width: 200px;">
                                        <div class="small">Source →</div>
                                        <div class="small">Target ↓</div>
                                    </th>
                                    <th v-for="(source, sIdx) in demoSources" :key="sIdx"
                                        class="bg-black text-white text-center border-dark py-3"
                                        style="min-width: 300px;">
                                        <div class="fw-bold mb-2">{{ source.name }}</div>
                                        <audio :src="source.url" controls class="w-100" style="height: 32px;"></audio>
                                    </th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="(target, tIdx) in demoTargets" :key="tIdx" class="border-dark">
                                    <!-- Target Audio Header -->
                                    <td class="bg-black text-white text-center border-dark py-3">
                                        <div class="fw-bold mb-2">{{ target.name }}</div>
                                        <audio :src="target.url" controls class="w-100" style="height: 32px;"></audio>
                                    </td>

                                    <!-- Voice Conversion Results -->
                                    <td v-for="(source, sIdx) in demoSources" :key="sIdx" class="p-3 border-dark">
                                        <div v-if="demoResults[tIdx] && demoResults[tIdx][sIdx]" class="bg-white">
                                            <!-- Model Labels -->
                                            <div class="row g-0 mb-2">
                                                <div class="col-6 text-center">
                                                    <small class="text-black fw-bold text-uppercase"
                                                        style="font-size: 0.7rem; letter-spacing: 0.5px;">
                                                        Model A
                                                    </small>
                                                </div>
                                                <div class="col-6 text-center">
                                                    <small class="text-black fw-bold text-uppercase"
                                                        style="font-size: 0.7rem; letter-spacing: 0.5px;">
                                                        Model B
                                                    </small>
                                                </div>
                                            </div>

                                            <!-- Audio Results -->
                                            <div class="row g-2">
                                                <div class="col-6">
                                                    <div class="border p-2">
                                                        <audio v-if="demoResults[tIdx][sIdx].left"
                                                            :src="demoResults[tIdx][sIdx].left" controls class="w-100"
                                                            style="height: 32px;"></audio>
                                                    </div>
                                                </div>
                                                <div class="col-6">
                                                    <div class="border p-2">
                                                        <audio v-if="demoResults[tIdx][sIdx].right"
                                                            :src="demoResults[tIdx][sIdx].right" controls class="w-100"
                                                            style="height: 32px;"></audio>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>

                                        <!-- Placeholder -->
                                        <div v-else class="text-center py-4">
                                            <div class="text-black-50 small">Loading audio...</div>
                                        </div>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
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
    'DarkStream-v2-logits',
    'DarkStream-bottleneck-tvtimbre',
    'DarkStream-bottleneckvq-tvtimbre',
    'DarkStreamTVT-m1',
    'GenVC-small',
    'GenVC-large',
    'GenVC-small-nonstreaming',
    'GenVC-large-nonstreaming'
]
const modelInfos = {
    'DarkStream-v2-logits': {
        latency: 'TODO',
        rtf: 'TODO',
    },
    'DarkStream-bottleneck-tvtimbre': {
        latency: 'TODO',
        rtf: 'TODO',
    },
    'DarkStream-bottleneckvq-tvtimbre': {
        latency: 'TODO',
        rtf: 'TODO',
    },
    'DarkStreamTVT-m1': {
        latency: 'TODO',
        rtf: 'TODO',
    },
    'GenVC-small': {
        latency: '0.29 ± 0.03',
        rtf: '0.83 ± 0.05',
    },
    'GenVC-large': {
        latency: '0.32 ± 0.11',
        rtf: '0.83 ± 0.07',
    },
    'GenVC-small-nonstreaming': {
        latency: 'None',
        rtf: 'None',
    },
    'GenVC-large-nonstreaming': {
        latency: 'None',
        rtf: 'None',
    },
}

const leftModel = ref('DarkStream-v2-logits')
const rightModel = ref('DarkStreamTVT-m1')

// Mode selection
const currentMode = ref('demo')

// Upload mode data
const sourceAudioUrl = ref(null)
const targetAudioUrl = ref(null)
const leftResult = ref(null)
const rightResult = ref(null)
const isProcessing = ref(false)

// Demo mode data
const demoResults = ref({}) // Store results for each target-source combination
const evaluations = ref({}) // Store user evaluations

// Demo audio files - organized structure
const demoSources = ref([
    { name: 'RRBI', url: getAssetUrl('/audio/demo/sources/RRBI_arctic_a0055.wav') },
    { name: 'TNI', url: getAssetUrl('/audio/demo/sources/TNI_arctic_a0356.wav') },
    { name: 'BDL', url: getAssetUrl('/audio/demo/sources/BDL_arctic_a0406.wav') },
    { name: 'MBMPS', url: getAssetUrl('/audio/demo/sources/MBMPS_arctic_b0244.wav') },
    { name: 'CLB', url: getAssetUrl('/audio/demo/sources/CLB_arctic_b0322.wav') }
])

const demoTargets = ref([
    { name: 'ERMS', url: getAssetUrl('/audio/demo/targets/ERMS_arctic_a0113.wav') },
    { name: 'ASI', url: getAssetUrl('/audio/demo/targets/ASI_arctic_a0292.wav') },
    { name: 'SLT', url: getAssetUrl('/audio/demo/targets/SLT_arctic_a0334.wav') },
    { name: 'SVBI', url: getAssetUrl('/audio/demo/targets/SVBI_arctic_a0508.wav') },
    { name: 'NJS', url: getAssetUrl('/audio/demo/targets/NJS_arctic_b0170.wav') }
])

// File upload handlers
const handleSourceUpload = (event) => {
    const file = event.target.files[0]
    if (file) {
        sourceAudioUrl.value = URL.createObjectURL(file)
    }
}

const handleTargetUpload = (event) => {
    const file = event.target.files[0]
    if (file) {
        targetAudioUrl.value = URL.createObjectURL(file)
    }
}

// Voice conversion functions
const performVC = async (side) => {
    isProcessing.value = true
    try {
        // TODO: Replace with actual API call to your VC backend
        await new Promise(resolve => setTimeout(resolve, 2000)) // Simulate processing

        // Mock result - replace with actual result from API
        const mockResult = getAssetUrl('/demo/result_mock.wav')

        if (side === 'left') {
            leftResult.value = mockResult
        } else {
            rightResult.value = mockResult
        }
    } catch (error) {
        console.error('Voice conversion failed:', error)
    } finally {
        isProcessing.value = false
    }
}

// Generate voice conversion for demo mode
const generateDemoVC = async (targetIdx, sourceIdx) => {
    isProcessing.value = true
    try {
        // TODO: Replace with actual API call to your VC backend
        await new Promise(resolve => setTimeout(resolve, 2000)) // Simulate processing

        // Initialize nested object if it doesn't exist
        if (!demoResults.value[targetIdx]) {
            demoResults.value[targetIdx] = {}
        }

        // Get basenames for more readable filenames
        const sourceName = demoSources.value[sourceIdx].url.split('/').pop().replace('.wav', '')
        const targetName = demoTargets.value[targetIdx].url.split('/').pop().replace('.wav', '')

        // Mock results - replace with actual results from API
        demoResults.value[targetIdx][sourceIdx] = {
            left: getAssetUrl(`/audio/demo/results/${leftModel.value}/${targetName}/${sourceName}.wav`),
            right: getAssetUrl(`/audio/demo/results/${rightModel.value}/${targetName}/${sourceName}.wav`)
        }

        // Force reactivity update
        demoResults.value = { ...demoResults.value }

    } catch (error) {
        console.error('Voice conversion failed:', error)
    } finally {
        isProcessing.value = false
    }
}

// Generate all demo combinations at once
const generateAllDemoVC = async () => {
    isProcessing.value = true
    try {
        // TODO: Replace with actual batch API call to your VC backend
        // For now, simulate processing all combinations
        // await new Promise(resolve => setTimeout(resolve, 3000)) // Simulate longer processing for all

        const newResults = {}

        // Generate results for all combinations
        for (let tIdx = 0; tIdx < demoTargets.value.length; tIdx++) {
            newResults[tIdx] = {}
            for (let sIdx = 0; sIdx < demoSources.value.length; sIdx++) {
                // Get basenames for more readable filenames
                const sourceName = demoSources.value[sIdx].url.split('/').pop().replace('.wav', '')
                const targetName = demoTargets.value[tIdx].url.split('/').pop().replace('.wav', '')
                newResults[tIdx][sIdx] = {
                    left: getAssetUrl(`/audio/demo/results/${leftModel.value}/${targetName}/${sourceName}.wav`),
                    right: getAssetUrl(`/audio/demo/results/${rightModel.value}/${targetName}/${sourceName}.wav`)
                }
            }
        }

        demoResults.value = newResults

    } catch (error) {
        console.error('Batch voice conversion failed:', error)
    } finally {
        isProcessing.value = false
    }
}

// Mark which model performed better for a specific combination
const markBetter = (targetIdx, sourceIdx, choice) => {
    if (!evaluations.value[targetIdx]) {
        evaluations.value[targetIdx] = {}
    }

    evaluations.value[targetIdx][sourceIdx] = choice
    evaluations.value = { ...evaluations.value }

    console.log(`Target ${targetIdx}, Source ${sourceIdx}: ${choice} is better`)
}

// Watch for model changes and regenerate demo results
watch([leftModel, rightModel], () => {
    // Only regenerate if we're in demo mode and have existing results
    if (currentMode.value === 'demo' && Object.keys(demoResults.value).length > 0) {
        generateAllDemoVC()
    }
})

// Generate demo results when component mounts
onMounted(() => {
    // Auto-generate demo results on page load since we start in demo mode
    if (currentMode.value === 'demo') {
        generateAllDemoVC()
    }
})
</script>

<style scoped>
/* Bootstrap handles styling */
</style>
