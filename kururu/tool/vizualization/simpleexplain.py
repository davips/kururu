#  Copyright (c) 2020. Davi Pereira dos Santos
#  This file is part of the kururu project.
#  Please respect the license - more about this in the section (*) below.
#
#  kururu is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  kururu is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with kururu.  If not, see <http://www.gnu.org/licenses/>.
#
#  (*) Removing authorship by any means, e.g. by distribution of derived
#  works or verbatim, obfuscated, compiled or rewritten versions of any
#  part of this work is a crime and is unethical regarding the effort and
#  time spent here.
#  Relevant employers or funding agencies will be notified accordingly.

# from matplotlib import pyplot as plt
#
# from akangatu.ddstep import DDStep
# from melime.explainers.explainer import Explainer
# from melime.explainers.visualizations.plot_importance import ExplainGraph
# from melime.generators.kde_gen import KDEGen
# # from akangatu.transf.mixin.noop import asNoOp
#
#
# # TODO: simplify this class to be independent of the prediction of syntetic examples.
# class Explain(asNoOp, DDStep):
#     def __init__(self, inner=None, class_index=0):
#     raise NotImplemented
#     super().__init__(inner, {"class_index": class_index})
#     # TODO: dar opção de selecionar a classe mais forte, mas depende de passar o modelo (issue no melime?)
#     self.class_index = class_index
#
#     def _process_(self, data):
#     inner = data.inner
#     generator = KDEGen(verbose=True).fit(inner.X)
#     # TODO: model_predict depende do modelo pra predizer em exemplos artificiais
#     explainer = Explainer(
#         model_predict=??????????????????????????????,
#         generator=generator,
#         local_model='Ridge',
#         feature_names=data.Xd,
#         target_names=data.Yd
#     )
#     explanation, counterfactual_examples = explainer.explain_instance(
#         x_explain=data.X[0:1],
#         class_index=self.class_index,
#         r=1.0,
#         n_samples=500,
#         tol_importance=0.1,
#         tol_error=0.1,
#         local_mini_batch_max=40,
#         scale_data=False,
#         weight_kernel='gaussian'
#     )
#     fig, axs = ExplainGraph.plot(explanation.explain())
#     # plt.savefig(f'iris_x_{",".join(data.Xd)}_m-lime_kde.svg')
#     plt.show()  # pip install PyQt5==5.12.2  # plotlib is currently using agg, which is a non-GUI backend, so canno
#     fig, axs = ExplainGraph.plot_errors(explanation)
#
#     return data
