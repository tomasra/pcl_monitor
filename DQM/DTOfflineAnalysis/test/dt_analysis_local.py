import FWCore.ParameterSet.Config as cms

process = cms.Process("DTOffAna3")

#myoutputdir = '/data/c/cerminar/data/DtCalibrationGoodCollV9-100610-V10/'
myoutputdir = './'


# the source
process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring(
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_100_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_106_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_107_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_10_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_110_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_114_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_115_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_118_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_119_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_121_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_129_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_130_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_134_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_135_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_139_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_13_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_142_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_143_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_144_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_145_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_149_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_151_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_153_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_154_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_160_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_166_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_167_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_168_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_16_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_173_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_176_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_177_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_178_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_179_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_17_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_180_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_183_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_184_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_185_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_186_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_187_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_188_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_189_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_190_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_191_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_192_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_194_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_195_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_196_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_197_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_198_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_199_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_19_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_1_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_203_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_204_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_205_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_206_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_208_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_209_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_210_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_213_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_214_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_215_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_216_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_217_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_218_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_219_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_21_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_220_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_221_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_222_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_223_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_224_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_225_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_226_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_227_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_228_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_229_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_230_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_231_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_232_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_233_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_237_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_23_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_241_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_243_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_245_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_246_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_248_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_24_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_250_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_259_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_260_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_261_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_265_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_266_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_267_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_268_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_269_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_270_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_271_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_272_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_273_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_274_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_275_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_279_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_27_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_280_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_281_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_283_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_287_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_288_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_290_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_292_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_293_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_295_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_297_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_299_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_29_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_300_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_301_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_304_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_305_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_306_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_307_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_308_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_309_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_310_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_312_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_314_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_315_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_317_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_319_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_32_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_33_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_36_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_37_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_38_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_39_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_42_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_44_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_46_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_47_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_48_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_49_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_4_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_54_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_55_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_57_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_58_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_60_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_61_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_62_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_63_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_69_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_76_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_77_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_79_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_7_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_80_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_84_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_85_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_86_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_87_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_88_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_89_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_8_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_90_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_91_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_92_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_94_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_95_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_97_1.root',
'/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100610-V10/45d5a4add3c13836d9608259324344ab/good_coll_9_1.root'                                ))

process.source.inputCommands = cms.untracked.vstring("keep *", "drop *_MEtoEDMConverter_*_*", "drop L1GlobalTriggerObjectMapRecord_hltL1GtObjectMap__HLT")

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
    )


process.load('Configuration/StandardSequences/MagneticField_AutoFromDBCurrent_cff')
process.load('Configuration/StandardSequences/GeometryIdeal_cff')


process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = "GR_R_35X_V8::All"

                                            
# process.GlobalTag.toGet = cms.VPSet(
#     cms.PSet(record = cms.string("DTTtrigRcd"),
#              tag = cms.string("ttrig"),
#              connect = cms.untracked.string("sqlite_file:ttrigStat1_V0.db")
#              )
#     )



process.load("Configuration/StandardSequences/RawToDigi_Data_cff")
process.load("Configuration/StandardSequences/Reconstruction_cff")
process.load('Configuration/EventContent/EventContent_cff')

process.FEVTEventContent.outputCommands.append('drop *_MEtoEDMConverter_*_*')

process.load('L1TriggerConfig.L1GtConfigProducers.L1GtTriggerMaskAlgoTrigConfig_cff')
process.load('L1TriggerConfig.L1GtConfigProducers.L1GtTriggerMaskTechTrigConfig_cff')
process.load('HLTrigger/HLTfilters/hltLevel1GTSeed_cfi')


process.dtNDigiFilter = cms.EDFilter("DTNDigiFilter",
    threshold = cms.untracked.int32(10),
    debug = cms.untracked.bool(False),
    dtDigiLabel = cms.InputTag("muonDTDigis"),
    granularity = cms.untracked.string('perChamber'),
    cutType = cms.untracked.string('moreThan')
)

process.load('DQM.DTOfflineAnalysis.dtLocalRecoAnalysis_cfi')
process.dtLocalRecoAnal.rootFileName = myoutputdir + 'DTLocalRecoAnalysisStd.root'

####################################################################################
##################################good collisions############################################

process.L1T1coll=process.hltLevel1GTSeed.clone()
process.L1T1coll.L1TechTriggerSeeding = cms.bool(True)
process.L1T1coll.L1SeedsLogicalExpression = cms.string('0 AND (40 OR 41) AND NOT (36 OR 37 OR 38 OR 39) AND NOT ((42 AND NOT 43) OR (43 AND NOT 42))')

#process.l1tcollpath = cms.Path(process.L1T1coll*process.muonDTDigis*process.dtlocalreco*process.dtNDigiFilter+process.dtLocalRecoAnal)

process.primaryVertexFilter = cms.EDFilter("VertexSelector",
   src = cms.InputTag("offlinePrimaryVertices"),
   cut = cms.string("!isFake && ndof > 4 && abs(z) <= 15 && position.Rho <= 2"), # tracksSize() > 3 for the older cut
   filter = cms.bool(True),   # otherwise it won't filter the events, just produce an empty vertex collection.
)


process.noscraping = cms.EDFilter("FilterOutScraping",
applyfilter = cms.untracked.bool(True),
debugOn = cms.untracked.bool(False),
numtrack = cms.untracked.uint32(10),
thresh = cms.untracked.double(0.25)
)

#process.goodvertex=cms.Path(process.primaryVertexFilter+process.noscraping*process.muonDTDigis*process.dtlocalreco*process.dtNDigiFilter+process.dtLocalRecoAnal)


process.collout = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string(myoutputdir + 'good_coll.root'),
    outputCommands = process.FEVTEventContent.outputCommands,
    dataset = cms.untracked.PSet(
    	      dataTier = cms.untracked.string('RAW-RECO'),
    	      filterName = cms.untracked.string('GOODCOLL')),
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('goodvertex','l1tcollpath')
    )
)

# message logger
process.MessageLogger = cms.Service("MessageLogger",
                                    debugModules = cms.untracked.vstring('*'),
                                    destinations = cms.untracked.vstring('cout'),
                                    categories = cms.untracked.vstring('DTNoiseAnalysisTest'), 
                                    cout = cms.untracked.PSet(threshold = cms.untracked.string('DEBUG'),
                                                              noLineBreaks = cms.untracked.bool(False),
                                                              DEBUG = cms.untracked.PSet(
                                                                  limit = cms.untracked.int32(0)),
                                                              INFO = cms.untracked.PSet(
                                                                  limit = cms.untracked.int32(0)),
                                                              DTNoiseAnalysisTest = cms.untracked.PSet(
                                                                  limit = cms.untracked.int32(-1))
                                                              )
                                    )



process.recoonly = cms.Path(process.muonDTDigis+process.dt2DSegments+process.dtLocalRecoAnal) 

#process.outpath = cms.EndPath(process.collout)


process.recoout = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string(myoutputdir + 'good_coll.root'),
    outputCommands = process.FEVTEventContent.outputCommands,
    dataset = cms.untracked.PSet(
    	      dataTier = cms.untracked.string('RAW-RECO'),
    	      filterName = cms.untracked.string('GOODCOLL')),
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('recoonly')
    )
)


process.outpath = cms.EndPath(process.recoout)

process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True)
    )



# process.jobPath = cms.Path(process.reco + process.dtLocalRecoAnal)

#process.jobPath = cms.Path(process.dtLocalRecoAnal)


#f = file('aNewconfigurationFile.cfg', 'w')
#f.write(process.dumpConfig())
#f.close()

