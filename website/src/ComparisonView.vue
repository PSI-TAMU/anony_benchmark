<template>
    <div class="min-vh-100 bg-light p-4">
        <!-- Header -->
        <header class="d-flex justify-content-between align-items-center mb-4">
            <h1 class="h3 fw-semibold">Side by Side</h1>
            <button class="btn btn-link text-primary text-decoration-none">⚙️ Settings</button>
        </header>

        <!-- Mode Selection -->
        <div class="row mb-4">
            <div class="col-12">
                <div class="btn-group w-100" role="group">
                    <!-- <input type="radio" class="btn-check" name="mode" id="uploadMode" v-model="currentMode"
                        value="upload">
                    <label class="btn btn-outline-primary" for="uploadMode">Upload Mode</label> -->

                    <input type="radio" class="btn-check" name="mode" id="demoMode" v-model="currentMode" value="demo">
                    <label class="btn btn-outline-primary" for="demoMode">Demo Mode</label>
                </div>
                <p class="text-muted mt-2 mb-0">
                    <span v-if="currentMode === 'upload'">Upload your own source and target audio files</span>
                    <span v-else>Test with 5 source × 5 target = 25 predefined audio combinations</span>
                </p>
            </div>
        </div>

        <!-- Model Selection -->
        <div class="row mb-4">
            <div class="col-md-6">
                <label for="leftModel" class="form-label fw-semibold">Left Model</label>
                <select id="leftModel" class="form-select" v-model="leftModel">
                    <option v-for="model in availableModels" :key="model" :value="model">{{ model }}</option>
                </select>
            </div>
            <div class="col-md-6">
                <label for="rightModel" class="form-label fw-semibold">Right Model</label>
                <select id="rightModel" class="form-select" v-model="rightModel">
                    <option v-for="model in availableModels" :key="model" :value="model">{{ model }}</option>
                </select>
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
                            <input type="file" class="form-control mb-3" accept="audio/*" @change="handleSourceUpload">
                            <audio v-if="sourceAudioUrl" :src="sourceAudioUrl" controls class="w-100"></audio>
                        </div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-body">
                            <h5 class="card-title">Target Audio</h5>
                            <input type="file" class="form-control mb-3" accept="audio/*" @change="handleTargetUpload">
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
                                <button class="btn btn-primary" @click="performVC('left')" :disabled="isProcessing">
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
                                <button class="btn btn-primary" @click="performVC('right')" :disabled="isProcessing">
                                    {{ isProcessing ? 'Processing...' : 'Generate Voice Conversion' }}
                                </button>
                            </div>
                            <audio v-if="rightResult" :src="rightResult" controls class="w-100"></audio>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Demo Mode Content -->
        <div v-else>
            <div class="d-flex justify-content-between align-items-center mb-3">
                <h5 class="mb-0">Demo Mode: Source vs Target Speakers</h5>
                <button class="btn btn-primary" @click="generateAllDemoVC" :disabled="isProcessing">
                    {{ isProcessing ? 'Generating All...' : 'Generate All Combinations' }}
                </button>
            </div>
            <p class="text-muted mb-4">Each cell shows results from both models side by side. Use "Generate All" to
                create all 25 combinations at once.</p>

            <div class="table-responsive">
                <table class="table table-bordered align-middle">
                    <thead class="table-primary">
                        <tr>
                            <th class="bg-primary text-white text-center" style="min-width: 180px;">
                                <small>Source →</small><br>
                                <small>Target ↓</small>
                            </th>
                            <th v-for="(source, sIdx) in demoSources" :key="sIdx" class="text-center"
                                style="min-width: 300px;">
                                <div class="fw-semibold">{{ source.name }}</div>
                                <audio :src="source.url" controls class="mt-1"
                                    style="width: 280px; height: 30px;"></audio>
                            </th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(target, tIdx) in demoTargets" :key="tIdx">
                            <!-- Target Audio Header -->
                            <td class="bg-light text-center">
                                <div class="fw-semibold text-primary mb-2">{{ target.name }}</div>
                                <audio :src="target.url" controls style="width: 100%; height: 30px;"></audio>
                            </td>

                            <!-- Voice Conversion Results -->
                            <td v-for="(source, sIdx) in demoSources" :key="sIdx" class="p-2">
                                <div v-if="demoResults[tIdx] && demoResults[tIdx][sIdx]"
                                    class="border rounded p-2 bg-light">
                                    <!-- Side by Side Audio Results -->
                                    <div class="row g-1">
                                        <!-- Left Model Result -->
                                        <div class="col-6">
                                            <small class="fw-semibold text-success d-block text-center">{{ leftModel
                                                }}</small>
                                            <audio v-if="demoResults[tIdx][sIdx].left"
                                                :src="demoResults[tIdx][sIdx].left" controls class="w-100"
                                                style="height: 30px;"></audio>
                                        </div>

                                        <!-- Right Model Result -->
                                        <div class="col-6">
                                            <small class="fw-semibold text-info d-block text-center">{{ rightModel
                                                }}</small>
                                            <audio v-if="demoResults[tIdx][sIdx].right"
                                                :src="demoResults[tIdx][sIdx].right" controls class="w-100"
                                                style="height: 30px;"></audio>
                                        </div>
                                    </div>
                                </div>

                                <!-- Placeholder when no results -->
                                <div v-else class="text-center text-muted p-3">
                                    <small>Click "Generate All" to create voice conversion samples</small>
                                </div>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- Footer Buttons -->
        <div class="d-flex justify-content-center mt-4 gap-2">
            <button class="btn btn-secondary">⬅ Left is Better</button>
            <button class="btn btn-secondary">It's a tie</button>
            <button class="btn btn-secondary">➡ Right is Better</button>
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
    'GenVC-small',
    'GenVC-large'
]

const leftModel = ref('DarkStream-v2-logits')
const rightModel = ref('GenVC-small')

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
