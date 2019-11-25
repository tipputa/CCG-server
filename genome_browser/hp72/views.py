from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from .models import GenbankSummary, ConsensusGroup, Genome
from .serializers import *
from django.shortcuts import get_object_or_404, get_list_or_404


""" genome ID """
## all
class RetrieveAllByGenomeIDFromGB(generics.ListAPIView):
    serializer_class = RetrieveAllFromGBSerializer
    def get_queryset(self):
        return GenbankSummary.objects.filter(genome_ID=self.kwargs["genome_ID"])

""" locus tag """
## all
class RetrieveAllByLocusTagFromGB(generics.ListAPIView):
    serializer_class = RetrieveAllFromGBSerializer
    def get_queryset(self):
        return [GenbankSummary.objects.get(locus_tag=self.kwargs["locusTag"])]

## position
class RetrievePositionByLocusTagFromGB(generics.ListAPIView):
    serializer_class = RetrievePositionsFromGBSerializer
    def get_queryset(self):
        return [GenbankSummary.objects.get(locus_tag=self.kwargs["locusTag"])]

## protein sequence
class RetrieveProteinByLocusTagFromGB(generics.ListAPIView):
    serializer_class = RetrieveProteinFromGBSerializer
    def get_queryset(self):
        return [GenbankSummary.objects.get(locus_tag=self.kwargs["locusTag"])]

## CDS
class RetrieveCodingSeqByLocusTagFromGB(generics.ListAPIView):
    serializer_class = RetrieveCodingSeqFromGBSerializer
    def get_queryset(self):
        return [GenbankSummary.objects.get(locus_tag=self.kwargs["locusTag"])]


""" test  """
class RetrieveTest(generics.ListAPIView):
    serializer_class = RetrievePositionsFromGBSerializer
    def get_queryset(self):
        return GenbankSummary.objects.all()[:self.kwargs["num"]]

""" Genome """
class RetrieveAllGenome(generics.ListAPIView):
    serializer_class = RetrieveAllFromGenomeSerializer
    def get_queryset(self):
        return Genome.objects.filter(genome_ID=self.kwargs["genome_ID"])

class RetrieveTargetGenomicRegion(generics.ListAPIView):
    serializer_class = RetrieveAllFromGenomeSerializer
    def get_queryset(self):
        return Genome.objects.filter(genome_ID=self.kwargs["genome_ID"]).exclude(end__lte=self.kwargs["start"]).exclude(start__gte=self.kwargs["end"])

class RetriveTest(APIView):
    def post(self, request, *args, **kwargs):
        #self.queryset = GenbankSummary.objects.all()[:self.request.data["num"]]
        #for seq in data = self.request.data["seqs"]:
        #    Genome.objects.filter(genome_ID=self.kwargs["genome_ID"]).filter(start__lt=self.kwargs["start"]).filter(end__gt=self.kwargs["end"])[:1]            

        all_res = [CommentSerializer(get_list_or_404(Genome.objects.filter(genome_ID=seq["genome_ID"]).exclude(end__lt=seq["start"]).exclude(start__gt=seq["end"])), many=True).data for seq in self.request.data["seqs"]]

        """ this is too slow
        seq = self.request.data["seqs"][0]
        p2 = Genome.objects.filter(genome_ID=seq["genome_ID"]).filter(start__lte=seq["start"]).filter(end__gte=seq["end"])[:1]
        for seq in self.request.data["seqs"][1:]:
            p1 = Genome.objects.filter(genome_ID=seq["genome_ID"]).filter(start__lte=seq["start"]).filter(end__gte=seq["end"])[:1]
            p2 = p2 | p1

        all_res = CommentSerializer(get_list_or_404(p2), many=True).data
        """
        res = {}        
        for value_arr in all_res:
            value_arr_sorted = sorted(value_arr, key=lambda x:x['start'])
            for values in value_arr_sorted:
                key = values.pop("genome_ID")
                if key in res:
                    res[key]["end"] = values["end"]
                    res[key]["seq"] += values["seq"]
                else:
                    res[key] = values

        return Response(res);

class RetriveConsensusGroup(generics.ListAPIView):
    serializer_class = RetriveSameConsensusGroup
    def get_queryset(self):
        #return ConsensusGroup.objects.filter(consensus_id=self.kwargs["consensus_id"])
        return ConsensusGroup.objects.filter(consensus_id=self.kwargs["consensus_id"])

    def get(self, request, *args, **kwargs):
        lists = get_list_or_404(self.get_queryset())
        l2 = [GenbankSummary.objects.get(locus_tag=i.locus_tag) for i in lists]
        serializer = RetriveSameConsensusGroup(l2, many=True)
        res = {}
        for values in serializer.data:
            key = values.pop("genome_ID").replace(".gb", "")
            res[key] = values
        return Response(res)

class RetriveTest2(generics.ListAPIView):
    serializer_class = RetrievePositionsFromGBSerializer
    # parser_classes = [JSONParser] # default
    serializer_class = RetrieveAllFromGenomeSerializer
    def get_queryset(self):
        return Genome.objects.filter(genome_ID=self.kwargs["genome_ID"]).exclude(end__lte=self.kwargs["start"]).exclude(start__gte=self.kwargs["end"])

