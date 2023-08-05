import os
import platform
import sys
import numpy as np

from Bio.PDB.DSSP import *
from Bio.PDB.PDBParser import *
from Bio.PDB.Polypeptide import *
from scipy.spatial.distance import *

from contactlib.data_manger import asset_path


def loadPDB(pdbfn, fraglen=4, mingap=0, mincont=2, maxdist=16.0):
  if platform.system() == "Darwin":
    dssp_exe = asset_path("dssp-2.0.4-macOS")
  elif platform.system() == "Linux":
    dssp_exe = asset_path("dssp-2.0.4-linux-amd64")
  else:
    raise Exception("Unsupported platform! Please try it under Linux.")

  model = PDBParser(PERMISSIVE=1).get_structure("XXXX", pdbfn)[0]
  dsspfn = pdbfn.replace(".pdb", ".dssp")
  if os.path.isfile(dsspfn): dssp, keys = make_dssp_dict(dsspfn)
  else: dssp, keys = dssp_dict_from_pdb_file(pdbfn, DSSP=dssp_exe)

  idx, res, ss, coord = [], [], [], []
  for k in keys:
    try:
      i, r, s, c = k[1][1], dssp[k][0], dssp[k][1], model[k[0]][k[1]]["CA"].get_coord()
      idx.append(i)
      res.append(r)
      ss.append(s)
      coord.append(c)
    except KeyError: pass
  idx = np.array(idx)
  res = np.array(res)
  ss = np.array(ss)
  coord = np.array(coord)
  dist = squareform(pdist(coord))

  data = []
  for j in range(fraglen+mingap, len(dist)-fraglen + 1):
    for i in range(j-fraglen-mingap + 1):
      if np.any(dist[i:i+fraglen, i:i+fraglen] >= maxdist): continue
      if np.any(dist[j:j+fraglen, j:j+fraglen] >= maxdist): continue

      if np.any(dist[i:i+fraglen, j:j+fraglen] >= maxdist): continue
      if np.sum(dist[i:i+fraglen, j:j+fraglen] <= 8.0) < mincont: continue

      k = np.concatenate((idx[i:i+fraglen], idx[j:j+fraglen]), axis=0)
      r = np.concatenate((res[i:i+fraglen], res[j:j+fraglen]), axis=0)
      s = np.concatenate((ss[i:i+fraglen], ss[j:j+fraglen]), axis=0)
      c = np.concatenate((coord[i:i+fraglen], coord[j:j+fraglen]), axis=0)
      d0 = np.concatenate((dist[i:i+fraglen, i:i+fraglen], dist[i:i+fraglen, j:j+fraglen]), axis=1)
      d1 = np.concatenate((dist[j:j+fraglen, i:i+fraglen], dist[j:j+fraglen, j:j+fraglen]), axis=1)
      d = squareform(np.concatenate((d0, d1), axis=0))

      data.append([d, c, r, s, k])
  data = np.array(data)

  if len(data) > 0: return np.stack(data[:, 0]), np.stack(data[:, 1]), np.stack(data[:, 2]), np.stack(data[:, 3]), np.stack(data[:, 4]), len(res), len(data)
  else: return None, None, None, None, None, len(res), len(data)

def encode(ss):
  a, b, c = 0, 0, 0
  for i in ss:
    if i in "H": a += 1
    elif i in "E": b += 1
    else: c += 1
  if a >= 2 and a+c >=3: return "A%d" % a
  elif b >= 2 and b+c >=3: return "B%d" % b
  elif c >= 3: return "C%d" % c
  else: return "D0";

def filter(ss, lst):
  index = []
  fraglen = int(ss.shape[-1] / 2) # In Python3, fraglen is float due to division.
  for i in ss:
    code0 = encode(i[:fraglen])
    code1 = encode(i[-fraglen:])
    code = "".join(sorted([code0, code1]))
    index.append(code in lst)
  return index

